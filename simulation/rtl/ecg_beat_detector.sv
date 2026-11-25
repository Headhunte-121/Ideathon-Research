// R-peak detector and per-beat heart rate from a sampled ECG (fs = FS Hz).
// v2: works on the SLOPE of the ECG (sample minus the sample 12 ms earlier), which removes slow baseline wander
// (breathing, electrode drift) that fooled the first version on a drifting baseline.
// Adaptive threshold = 5/8 of a slowly decaying slope envelope, with a floor so that a flat
// (asystole or lifted-electrode) trace cannot trigger on noise. 0.3 s refractory period.
// hr_q4 = bpm * 16. Uses a divider; fine for simulation, replace by a sequential divider for synthesis.
module ecg_beat_detector #(
    parameter FS      = 250,
    parameter MIN_THR = 1500,
    parameter DECAY_SH = 10,       // envelope decay per sample = env >> DECAY_SH
    parameter SLOPE_N  = 3         // slope span in samples (3 at 250 Hz = 12 ms)
)(
    input  wire               clk, rst_n, sample_en,
    input  wire signed [15:0] ecg,
    output reg                beat,       // one clk pulse per detected beat that has a valid RR
    output reg  [15:0]        hr_q4
);
    reg [15:0] env, rr_cnt, refr;
    reg        have_prev;
    reg signed [15:0] h1, h2, h3;                          // sample history for the slope
    wire signed [16:0] sl = $signed({ecg[15], ecg}) - $signed({(SLOPE_N==1 ? h1[15] : SLOPE_N==2 ? h2[15] : h3[15]), (SLOPE_N==1 ? h1 : SLOPE_N==2 ? h2 : h3)});
    wire [16:0] sl_abs = sl[16] ? (~sl + 1'b1) : sl;
    wire [15:0] a   = (sl_abs > 17'd65535) ? 16'hFFFF : sl_abs[15:0];
    wire [15:0] thr0 = (env >> 1) + (env >> 3);           // 5/8 of envelope
    wire [15:0] thr  = (thr0 < MIN_THR) ? MIN_THR : thr0;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            env <= 0; rr_cnt <= 0; refr <= 0; have_prev <= 0; beat <= 0; hr_q4 <= 0; h1 <= 0; h2 <= 0; h3 <= 0;
        end else begin
            beat <= 0;
            if (sample_en) begin
                if (rr_cnt != 16'hFFFF) rr_cnt <= rr_cnt + 1;
                if (refr != 0) refr <= refr - 1;
                h1 <= ecg; h2 <= h1; h3 <= h2;
                if (a > env) env <= a; else env <= env - (env >> DECAY_SH);
                if (rr_cnt > 2 * FS) have_prev <= 0;      // no beat for 2 s: forget the last one
                if (a > thr && refr == 0) begin
                    refr <= (FS * 3) / 10;
                    rr_cnt <= 0;
                    have_prev <= 1;
                    if (have_prev && rr_cnt >= (FS * 3) / 10) begin
                        hr_q4 <= (60 * FS * 16) / rr_cnt;
                        beat  <= 1;
                    end
                end
            end
        end
    end
endmodule
