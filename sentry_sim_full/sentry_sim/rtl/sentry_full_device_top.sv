// End-to-end Sentry chain from raw sampled sensor signals to the outputs:
//   scg + motion ref -> NLMS cleaner -> chest-activity summary
//   ecg -> R-peak detector -> heart rate per beat -> (rest-only gate) -> drift detector
//   ppg -> wrist pulse size
//   drift_flag / pulse_loss / chest_still -> state machine -> haptic, call_req, siren, CPR beat
module sentry_full_device_top #(
    parameter CLK_HZ  = 100_000_000,
    parameter FS      = 250,
    parameter LOG2N   = 11,
    parameter WIN     = 60,
    parameter WIN_THR = 30,
    parameter CONSEC  = 5,
    parameter K2X16   = 230,
    parameter GATE_EN = 1,          // 1: ignore beats while the wearer is moving (rest-only baseline)
    parameter PP_THR  = 16'd1500,   // wrist pulse size below this = no pulse   (placeholder)
    parameter SCG_THR = 16'd40,     // cleaned chest activity below this = no heartbeat (placeholder)
    parameter MOV_THR = 16'd500,    // motion energy above this = moving (placeholder)
    parameter COOL_S  = 300,
    parameter REARM_S = 60
)(
    input  wire               clk, rst_n, sample_en,
    input  wire signed [15:0] ecg, scg, ppg, mot_ref,
    input  wire               cancel_btn, ack_btn, phone_link, impact_g3,
    output wire               haptic, call_req, siren_en, cpr_beat, drift_flag, learned,
    output wire [5:0]         countdown,
    output wire [2:0]         state_o,
    output wire [15:0]        hr_q4, ppg_pp, scg_energy, mov_energy,
    output wire               beat
);
    wire signed [15:0] scg_clean;
    wire               scg_valid;
    motion_noise_canceller #(.MU_SHIFT(2)) u_nlms (.clk(clk), .rst_n(rst_n), .in_valid(sample_en),
        .d(scg), .r(mot_ref), .e_out(scg_clean), .out_valid(scg_valid));

    ecg_beat_detector #(.FS(FS)) u_beat (.clk(clk), .rst_n(rst_n), .sample_en(sample_en),
        .ecg(ecg), .beat(beat), .hr_q4(hr_q4));

    signal_summary_1s #(.FS(FS)) u_stats (.clk(clk), .rst_n(rst_n), .sample_en(sample_en),
        .ppg(ppg), .ref_s(mot_ref), .scg_clean(scg_clean), .scg_valid(scg_valid),
        .ppg_pp(ppg_pp), .scg_energy(scg_energy), .mov_energy(mov_energy));

    wire moving     = (mov_energy > MOV_THR);
    wire plausible  = (hr_q4 >= 16'd480) && (hr_q4 <= 16'd3200);     // 30 to 200 bpm
    wire beat_ok    = beat && plausible && (GATE_EN ? !moving : 1'b1);

    baseline_drift_detector #(.LOG2N(LOG2N), .WIN(WIN), .WIN_THR(WIN_THR), .CONSEC(CONSEC), .K2X16(K2X16)) u_drift (
        .clk(clk), .rst_n(rst_n), .beat_valid(beat_ok), .hr_q4(hr_q4),
        .learned(learned), .drift_flag(drift_flag));

    wire pulse_loss  = (ppg_pp     < PP_THR);
    wire chest_still = (scg_energy < SCG_THR);

    alarm_state_machine #(.CLK_HZ(CLK_HZ), .COOL_S(COOL_S), .REARM_S(REARM_S)) u_fsm (
        .clk(clk), .rst_n(rst_n), .drift_flag(drift_flag), .pulse_loss(pulse_loss),
        .chest_still(chest_still), .cancel_btn(cancel_btn), .ack_btn(ack_btn),
        .phone_link(phone_link), .impact_g3(impact_g3), .haptic(haptic),
        .countdown(countdown), .call_req(call_req), .siren_en(siren_en),
        .cpr_beat(cpr_beat), .state_o(state_o));
endmodule
