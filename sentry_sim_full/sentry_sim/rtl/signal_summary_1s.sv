// Once-per-second summaries from sampled signals (FS samples per window):
//   ppg_pp     = wrist pulse size (peak-to-peak of the PPG)
//   scg_energy = mean |cleaned chest vibration|   (is there a heartbeat in the chest?)
//   mov_energy = mean |motion reference|          (is the wearer moving?)
module signal_summary_1s #(parameter FS = 250)(
    input  wire               clk, rst_n, sample_en,
    input  wire signed [15:0] ppg, ref_s, scg_clean,
    input  wire               scg_valid,
    output reg  [15:0]        ppg_pp, scg_energy, mov_energy
);
    reg [8:0]         n;
    reg signed [15:0] mx, mn;
    reg [31:0]        sum_s, sum_r;
    wire [15:0] as = scg_clean[15] ? (~scg_clean + 1'b1) : scg_clean;
    wire [15:0] ar = ref_s[15]     ? (~ref_s + 1'b1)     : ref_s;
    reg signed [16:0] pp;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            n <= 0; mx <= -16'sd32768; mn <= 16'sd32767; sum_s <= 0; sum_r <= 0;
            ppg_pp <= 16'hFFFF; scg_energy <= 16'hFFFF; mov_energy <= 0;   // start "alive, still unknown"
        end else begin
            if (scg_valid) sum_s <= sum_s + as;
            if (sample_en) begin
                if (ppg > mx) mx <= ppg;
                if (ppg < mn) mn <= ppg;
                sum_r <= sum_r + ar;
                if (n == FS - 1) begin
                    pp = mx - mn;
                    ppg_pp     <= (pp > 17'sd65535) ? 16'hFFFF : pp[15:0];
                    scg_energy <= sum_s / FS;
                    mov_energy <= sum_r / FS;
                    n <= 0; mx <= -16'sd32768; mn <= 16'sd32767; sum_s <= 0; sum_r <= 0;
                end else n <= n + 1;
            end
        end
    end
endmodule
