// R-peak detector and per-beat heart rate from a sampled ECG (fs = FS Hz).
// Adaptive threshold = 5/8 of a slowly decaying peak envelope, with a floor so that a flat
// (asystole or lifted-electrode) trace cannot trigger on noise. 0.3 s refractory period.
// hr_q4 = bpm * 16. Uses a divider; fine for simulation, replace by a sequential divider for synthesis.
module ecg_beat_detector #(
    parameter FS      = 250,
    parameter MIN_THR = 1500
)(
    input  wire               clk, rst_n, sample_en,
    input  wire signed [15:0] ecg,
    output reg                beat,       // one clk pulse per detected beat that has a valid RR
    output reg  [15:0]        hr_q4
);
    reg [15:0] env, rr_cnt, refr;
    reg        have_prev;
    wire [15:0] a   = ecg[15] ? (~ecg + 1'b1) : ecg;
    wire [15:0] thr0 = (env >> 1) + (env >> 3);           // 5/8 of envelope
    wire [15:0] thr  = (thr0 < MIN_THR) ? MIN_THR : thr0;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            env <= 0; rr_cnt <= 0; refr <= 0; have_prev <= 0; beat <= 0; hr_q4 <= 0;
        end else begin
            beat <= 0;
            if (sample_en) begin
                if (rr_cnt != 16'hFFFF) rr_cnt <= rr_cnt + 1;
                if (refr != 0) refr <= refr - 1;
                if (a > env) env <= a; else env <= env - (env >> 7);
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
