// 16-tap NLMS adaptive noise canceller, Q1.15 data, weights Q3.15 (18-bit).
// d = chest signal with motion noise, r = motion reference; e_out = cleaned signal.
// The 1/power division is replaced by a shift of the power's bit length (approximate NLMS).
// Written for clarity (all taps in one cycle), not for minimum area.
module nlms16 #(parameter MU_SHIFT = 2)(
    input  wire               clk, rst_n, in_valid,
    input  wire signed [15:0] d, r,
    output reg  signed [15:0] e_out,
    output reg                out_valid
);
    reg signed [15:0] xd [0:15];
    reg signed [15:0] xn [0:15];
    reg signed [17:0] w  [0:15];
    integer i, j, bl;
    reg signed [47:0] acc, pw, yv, ev, upd;
    reg signed [47:0] sat;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < 16; i = i + 1) begin xd[i] = 0; w[i] = 0; end
            e_out <= 0; out_valid <= 0;
        end else begin
            out_valid <= 0;
            if (in_valid) begin
                xn[0] = r;
                for (i = 1; i < 16; i = i + 1) xn[i] = xd[i-1];
                acc = 0; pw = 1;
                for (i = 0; i < 16; i = i + 1) begin
                    acc = acc + w[i] * xn[i];
                    pw  = pw + xn[i] * xn[i];
                end
                yv = acc >>> 15;
                ev = d - yv;
                sat = (ev > 32767) ? 48'sd32767 : (ev < -32768) ? -48'sd32768 : ev;
                bl = 0;
                for (j = 0; j < 48; j = j + 1) if (pw[j]) bl = j + 1;
                for (i = 0; i < 16; i = i + 1) begin
                    upd = ((sat * xn[i]) <<< 15) >>> (bl + MU_SHIFT);
                    w[i] = w[i] + upd;
                end
                for (i = 0; i < 16; i = i + 1) xd[i] = xn[i];
                e_out <= sat[15:0];
                out_valid <= 1;
            end
        end
    end
endmodule
