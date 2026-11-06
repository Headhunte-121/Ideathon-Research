// Baseline-drift detector. One feature value per heartbeat (heart rate in bpm*16, Q12.4).
// Learns mean/variance over 2^LOG2N beats, then flags SUSTAINED drift:
// a window of WIN beats is "bad" if >= WIN_THR beats lie beyond K sigma;
// CONSEC bad windows in a row raise drift_flag; CLEAN good windows clear it.
// K is given as K2X16 = K*K*16 (3.8 sigma -> 230). No division in the detection path.
module drift_det #(
    parameter LOG2N     = 11,
    parameter WIN       = 60,
    parameter WIN_THR   = 30,
    parameter CONSEC    = 5,
    parameter CLEAN     = 2,
    parameter K2X16     = 230,
    parameter VAR_FLOOR = 256,  // (1 bpm*16)^2, stops a flat baseline giving zero variance
    parameter ADAPT_SHIFT = 0   // 0 = fixed baseline; n = slow adaptation, alpha = 2^-n (non-exceeding beats only)
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        beat_valid,
    input  wire [15:0] hr_q4,
    output reg         learned,
    output reg         drift_flag
);
    localparam integer N = (1 << LOG2N);

    reg [LOG2N:0]      cnt;
    reg [63:0]         sum, sumsq;
    reg                fin;
    reg signed [63:0]  mean, var_r;
    reg [15:0]         wcnt, ecnt;
    reg [7:0]          consec, cleanw;

    reg signed [63:0] x, d, d2, lhs, rhs, vv;
    reg               exceed;
    reg [15:0]        tot;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt <= 0; sum <= 0; sumsq <= 0; fin <= 0; learned <= 0; drift_flag <= 0;
            mean <= 0; var_r <= VAR_FLOOR; wcnt <= 0; ecnt <= 0; consec <= 0; cleanw <= 0;
        end else begin
            if (fin) begin
                mean   <= $signed(sum >> LOG2N);
                var_r  <= $signed(sumsq >> LOG2N) - $signed(sum >> LOG2N) * $signed(sum >> LOG2N);
                learned <= 1; fin <= 0;
            end
            if (beat_valid) begin
                x = {48'd0, hr_q4};
                if (!learned && !fin) begin
                    sum <= sum + x; sumsq <= sumsq + x * x; cnt <= cnt + 1;
                    if (cnt == N - 1) fin <= 1;
                end else if (learned) begin
                    d  = x - mean;
                    d2 = d * d;
                    vv = (var_r < VAR_FLOOR) ? VAR_FLOOR : var_r;
                    lhs = d2 * 16;
                    rhs = K2X16 * vv;
                    exceed = (lhs > rhs);
                    if (ADAPT_SHIFT > 0 && !exceed) begin
                        mean  <= mean + ((d + (64'sd1 <<< (ADAPT_SHIFT-1))) >>> ADAPT_SHIFT);  // rounded, so no downward bias
                        var_r <= var_r + ((d2 - var_r + (64'sd1 <<< (ADAPT_SHIFT-1))) >>> ADAPT_SHIFT);
                    end
                    if (wcnt == WIN - 1) begin
                        tot = ecnt + (exceed ? 16'd1 : 16'd0);
                        if (tot >= WIN_THR) begin
                            cleanw <= 0;
                            consec <= consec + 1;
                            if (consec + 1 >= CONSEC) drift_flag <= 1;
                        end else begin
                            consec <= 0;
                            cleanw <= cleanw + 1;
                            if (cleanw + 1 >= CLEAN) drift_flag <= 0;
                        end
                        wcnt <= 0; ecnt <= 0;
                    end else begin
                        wcnt <= wcnt + 1;
                        if (exceed) ecnt <= ecnt + 1;
                    end
                end
            end
        end
    end
endmodule
