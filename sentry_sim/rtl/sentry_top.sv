// Decision chain of the Sentry: feature inputs -> drift detector + pulse-loss check -> state machine.
// ppg_pp = wrist pulse peak-to-peak per second; scg_energy = chest vibration energy per second.
module sentry_top #(
    parameter CLK_HZ  = 100_000_000,
    parameter LOG2N   = 11,
    parameter WIN     = 60,
    parameter WIN_THR = 30,
    parameter CONSEC  = 5,
    parameter K2X16   = 230,
    parameter PP_THR  = 16'd200,   // below this the wrist shows no pulse (placeholder)
    parameter SCG_THR = 16'd200,   // below this the chest is still (placeholder)
    parameter COOL_S  = 300,
    parameter REARM_S = 60
)(
    input  wire        clk, rst_n,
    input  wire        beat_valid,
    input  wire [15:0] hr_q4,
    input  wire [15:0] ppg_pp,
    input  wire [15:0] scg_energy,
    input  wire        cancel_btn, ack_btn, phone_link, impact_g3,
    output wire        haptic, call_req, siren_en, cpr_beat, drift_flag, learned,
    output wire [5:0]  countdown,
    output wire [2:0]  state_o
);
    drift_det #(.LOG2N(LOG2N), .WIN(WIN), .WIN_THR(WIN_THR), .CONSEC(CONSEC), .K2X16(K2X16)) u_drift (
        .clk(clk), .rst_n(rst_n), .beat_valid(beat_valid), .hr_q4(hr_q4),
        .learned(learned), .drift_flag(drift_flag));

    wire pulse_loss  = (ppg_pp    < PP_THR);
    wire chest_still = (scg_energy < SCG_THR);

    sentry_fsm #(.CLK_HZ(CLK_HZ), .COOL_S(COOL_S), .REARM_S(REARM_S)) u_fsm (
        .clk(clk), .rst_n(rst_n), .drift_flag(drift_flag), .pulse_loss(pulse_loss),
        .chest_still(chest_still), .cancel_btn(cancel_btn), .ack_btn(ack_btn),
        .phone_link(phone_link), .impact_g3(impact_g3), .haptic(haptic),
        .countdown(countdown), .call_req(call_req), .siren_en(siren_en),
        .cpr_beat(cpr_beat), .state_o(state_o));
endmodule
