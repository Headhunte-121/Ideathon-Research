// edge_cnn_beat: stand-alone Verilog copy of the beatnet-tiny INT8 integer network (spec: py/edge_int_model.py).
// NOT wired into pod_node.sv or any alarm logic.  Simulation-oriented: ROMs and activation buffers are plain arrays with combinational reads.
// One shared multiply-accumulate (int8 x int8 -> int32), one controller, two ping-pong activation buffers.
//   A (608 B): input window, then conv2 output.   B (600 B): conv1 output, then conv3 output.   (largest adjacent pair 600+608 = 1208 B)
// Accumulator bound: |acc| <= |bias| + cin*k*127*128 (< 2^20 for these layers; the testbench vectors reach about 1.1e5), so 32 bits are ample.
// Requantise: y = (acc*M0 + (1<<(n-1))) >>> n  (signed 64-bit product, arithmetic shift), clamp [0,127].
// Global pooling keeps the SUM of the 19 positions (no division).  score = logit1 - logit0.
// Protocol: pulse `start`; then present 75 int8 samples with in_valid=1 on 75 consecutive-or-not clocks; `done` pulses 1 clock when `score` is valid.
// Cycle accounting: 43,144 MAC cycles (zero-padding taps are counted as MAC cycles with x=0) + 1 init cycle per output element + 304 GAP-add cycles + a few.
module edge_cnn_beat #(parameter WDIR = "../rtl_edge/weights/") (
    input  wire              clk, rst_n, start, in_valid,
    input  wire signed [7:0] in_data,
    output reg               done, busy,
    output reg  signed [31:0] score,
    output reg  [31:0]       compute_cycles      // clocks from end of loading until done (all compute phases)
);
    // ---------------- ROMs ----------------
    reg signed [7:0]  w_rom  [0:1495];           // conv1 56 | conv2 640 | conv3 768 | fc 32
    reg signed [31:0] b_rom  [0:41];             // conv1 8 | conv2 16 | conv3 16 | fc 2
    reg        [31:0] m0_rom [0:39];
    reg        [7:0]  n_rom  [0:39];
    initial begin
        $readmemh({WDIR, "conv1_w.mem"}, w_rom, 0);    $readmemh({WDIR, "conv2_w.mem"}, w_rom, 56);
        $readmemh({WDIR, "conv3_w.mem"}, w_rom, 696);  $readmemh({WDIR, "fc_w.mem"},    w_rom, 1464);
        $readmemh({WDIR, "conv1_b.mem"}, b_rom, 0);    $readmemh({WDIR, "conv2_b.mem"}, b_rom, 8);
        $readmemh({WDIR, "conv3_b.mem"}, b_rom, 24);   $readmemh({WDIR, "fc_b.mem"},    b_rom, 40);
        $readmemh({WDIR, "conv1_m0.mem"}, m0_rom, 0);  $readmemh({WDIR, "conv2_m0.mem"}, m0_rom, 8);  $readmemh({WDIR, "conv3_m0.mem"}, m0_rom, 24);
        $readmemh({WDIR, "conv1_n.mem"},  n_rom, 0);   $readmemh({WDIR, "conv2_n.mem"},  n_rom, 8);   $readmemh({WDIR, "conv3_n.mem"},  n_rom, 24);
    end
    // ---------------- activation buffers (ping-pong) ----------------
    reg signed [7:0] bufA [0:607];
    reg signed [7:0] bufB [0:599];
    // ---------------- layer table (combinational) ----------------
    localparam S_IDLE = 0, S_LOAD = 1, S_INIT = 2, S_MAC = 3, S_GAP = 4, S_FINIT = 5, S_FMAC = 6, S_DONE = 7;
    reg [2:0]  st;
    reg [1:0]  layer;                            // 0 conv1, 1 conv2, 2 conv3
    reg [4:0]  co, ci;                           // output channel, input channel
    reg [6:0]  p;                                // output position
    reg [2:0]  j;                                // kernel tap
    reg [6:0]  lc;                               // load counter
    reg signed [31:0] acc;
    reg [8:0]  gi;                               // GAP counter 0..303
    reg signed [31:0] gsum [0:15];
    reg [4:0]  fj_c;  reg fj_o;                  // fc channel / output
    reg signed [31:0] logit0;

    reg [4:0] CIN, COUT; reg [2:0] K; reg [1:0] STRIDE; reg [2:0] PADL; reg [6:0] LIN, LOUT; reg [10:0] WBASE; reg [5:0] CBASE;
    always @* begin
        case (layer)
            2'd0: begin CIN = 1;  COUT = 8;  K = 7; STRIDE = 1; PADL = 3; LIN = 75; LOUT = 75; WBASE = 0;   CBASE = 0;  end
            2'd1: begin CIN = 8;  COUT = 16; K = 5; STRIDE = 2; PADL = 2; LIN = 75; LOUT = 38; WBASE = 56;  CBASE = 8;  end
            default: begin CIN = 16; COUT = 16; K = 3; STRIDE = 2; PADL = 0; LIN = 38; LOUT = 19; WBASE = 696; CBASE = 24; end
        endcase
    end
    // input position (signed) = p*STRIDE + j - PADL ; zero outside [0, LIN)
    wire signed [9:0] ipos = $signed({3'b0, p}) * $signed({8'b0, STRIDE}) + $signed({7'b0, j}) - $signed({7'b0, PADL});
    wire inr = (ipos >= 0) && (ipos < $signed({3'b0, LIN}));
    wire [10:0] raddr = ci * LIN + ipos[6:0];    // channel-major layout: index = ch*L + pos
    reg signed [7:0] xval;
    always @* begin
        xval = 8'sd0;
        if (inr) case (layer)
            2'd0: xval = bufA[raddr];            // input window (1 channel, 75)
            2'd1: xval = bufB[raddr];            // conv1 out
            default: xval = bufA[raddr];         // conv2 out
        endcase
    end
    wire [10:0] waddr = WBASE + (co * CIN + ci) * K + j;
    wire signed [7:0] wval = w_rom[waddr];
    wire signed [15:0] prod = xval * wval;
    wire signed [31:0] acc_next = acc + prod;
    wire last_tap = (j == K - 1) && (ci == CIN - 1);
    // requantise (used on the last tap, from acc_next)
    wire [5:0] cidx = CBASE + co;
    wire signed [63:0] rq_prod = acc_next * $signed({32'b0, m0_rom[cidx]});
    wire [7:0] nsh = n_rom[cidx];
    wire signed [63:0] rq_round = rq_prod + (64'sd1 <<< (nsh - 1));
    wire signed [63:0] rq_shift = rq_round >>> nsh;
    wire signed [7:0] yq = (rq_shift < 0) ? 8'sd0 : (rq_shift > 127) ? 8'sd127 : rq_shift[7:0];
    wire [10:0] oaddr = co * LOUT + p;
    // fc
    wire signed [7:0] fw = w_rom[1464 + fj_o * 16 + fj_c];
    wire signed [31:0] fprod = gsum[fj_c] * fw;
    integer ii;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= S_IDLE; done <= 0; busy <= 0; score <= 0; compute_cycles <= 0; layer <= 0; co <= 0; ci <= 0; p <= 0; j <= 0; lc <= 0; acc <= 0; gi <= 0; fj_c <= 0; fj_o <= 0; logit0 <= 0;
        end else begin
            done <= 0;
            if (st != S_IDLE && st != S_LOAD && st != S_DONE) compute_cycles <= compute_cycles + 1;
            case (st)
                S_IDLE: if (start) begin st <= S_LOAD; busy <= 1; lc <= 0; compute_cycles <= 0; end
                S_LOAD: if (in_valid) begin
                    bufA[lc] <= in_data;
                    if (lc == 74) begin st <= S_INIT; layer <= 0; co <= 0; p <= 0; ci <= 0; j <= 0; end else lc <= lc + 1;
                end
                S_INIT: begin acc <= b_rom[CBASE + co]; st <= S_MAC; end
                S_MAC: begin
                    if (last_tap) begin
                        case (layer) 2'd0: bufB[oaddr] <= yq; 2'd1: bufA[oaddr] <= yq; default: bufB[oaddr] <= yq; endcase
                        ci <= 0; j <= 0;
                        if (p == LOUT - 1) begin
                            p <= 0;
                            if (co == COUT - 1) begin
                                co <= 0;
                                if (layer == 2'd2) begin st <= S_GAP; gi <= 0; for (ii = 0; ii < 16; ii = ii + 1) gsum[ii] <= 0; end
                                else begin layer <= layer + 1; st <= S_INIT; end
                            end else begin co <= co + 1; st <= S_INIT; end
                        end else begin p <= p + 1; st <= S_INIT; end
                    end else begin
                        acc <= acc_next;
                        if (j == K - 1) begin j <= 0; ci <= ci + 1; end else j <= j + 1;
                    end
                end
                S_GAP: begin                      // gi = c*19 + pos over conv3 output (bufB, channel-major)
                    gsum[gi / 19] <= gsum[gi / 19] + bufB[gi];
                    if (gi == 303) begin st <= S_FINIT; fj_c <= 0; fj_o <= 0; end else gi <= gi + 1;
                end
                S_FINIT: begin acc <= b_rom[40 + fj_o]; fj_c <= 0; st <= S_FMAC; end
                S_FMAC: begin
                    if (fj_c == 15) begin
                        if (fj_o == 0) begin logit0 <= acc + fprod; fj_o <= 1; st <= S_FINIT; end
                        else begin score <= (acc + fprod) - logit0; st <= S_DONE; end
                    end else begin acc <= acc + fprod; fj_c <= fj_c + 1; end
                end
                S_DONE: begin done <= 1; busy <= 0; st <= S_IDLE; end
            endcase
        end
    end
endmodule
