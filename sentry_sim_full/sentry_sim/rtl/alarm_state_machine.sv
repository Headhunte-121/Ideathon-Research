// Sentry cancel-window state machine.
// MONITOR -> CHECKIN (drift only, haptic nudge, never calls)
// MONITOR/CHECKIN -> ARMED (pulse loss AND still chest held ARM_HOLD_S seconds)
// ARMED -> DISPATCH (countdown hits 0) -> SIREN_CPR; cancel or recovery returns to MONITOR
module alarm_state_machine #(
    parameter CLK_HZ     = 100_000_000, // set to 1000 in simulation so 1 "second" = 1000 clocks
    parameter ARM_HOLD_S = 3,
    parameter CANCEL_S   = 30,
    parameter CHECKIN_S  = 60,   // check-in timeout with no acknowledge
    parameter COOL_S     = 300,  // drift check-ins suppressed this long after ack/timeout
    parameter REARM_S    = 60    // arming blocked this long after a cancel or siren stop
)(
    input  wire       clk,
    input  wire       rst_n,
    input  wire       drift_flag,   // from baseline_drift_detector (check-in only)
    input  wire       pulse_loss,   // wrist PPG says no pulse
    input  wire       chest_still,  // chest shows no motion / no heartbeat vibration
    input  wire       cancel_btn,
    input  wire       ack_btn,
    input  wire       phone_link,
    input  wire       impact_g3,    // not used for control yet; reserved for siren gating
    output wire       haptic,
    output reg  [5:0] countdown,
    output wire       call_req,
    output wire       siren_en,
    output reg        cpr_beat,
    output wire [2:0] state_o
);
    localparam [2:0] S_MON = 3'd0, S_CHK = 3'd1, S_ARM = 3'd2, S_DISP = 3'd3, S_SIR = 3'd4;
    localparam integer CPR_HALF = (CLK_HZ / 1000) * 272;   // 110 BPM: 545 ms period

    reg [2:0]  state;
    reg [31:0] div, cdiv;
    reg [7:0]  arm_cnt, chk_cnt;
    reg [15:0] suppress, rearm;

    wire tick     = (div == CLK_HZ - 1);
    wire arm_cond = pulse_loss & chest_still;

    assign state_o  = state;
    assign haptic   = (state == S_CHK);
    assign siren_en = (state == S_DISP) || (state == S_SIR);
    assign call_req = siren_en & phone_link;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= S_MON; div <= 0; cdiv <= 0; arm_cnt <= 0; chk_cnt <= 0;
            suppress <= 0; rearm <= 0; countdown <= 0; cpr_beat <= 0;
        end else begin
            div <= tick ? 32'd0 : div + 1;

            // CPR metronome runs only while the siren state is active
            if (siren_en) begin
                if (cdiv >= CPR_HALF - 1) begin cdiv <= 0; cpr_beat <= ~cpr_beat; end
                else cdiv <= cdiv + 1;
            end else begin cdiv <= 0; cpr_beat <= 0; end

            if (tick) begin
                if (suppress != 0) suppress <= suppress - 1;
                if (rearm    != 0) rearm    <= rearm - 1;
                if ((state == S_MON || state == S_CHK) && arm_cond && rearm == 0)
                    arm_cnt <= arm_cnt + 1;
                else
                    arm_cnt <= 0;
            end

            case (state)
                S_MON: if (drift_flag && suppress == 0) begin state <= S_CHK; chk_cnt <= 0; end
                S_CHK: begin
                    if (ack_btn) begin state <= S_MON; suppress <= COOL_S; end
                    else if (tick) begin
                        chk_cnt <= chk_cnt + 1;
                        if (chk_cnt + 1 >= CHECKIN_S) begin state <= S_MON; suppress <= COOL_S; end
                    end
                end
                S_ARM: begin
                    if (cancel_btn) begin state <= S_MON; rearm <= REARM_S; countdown <= 0; end
                    else if (tick) begin
                        if (!arm_cond) begin state <= S_MON; countdown <= 0; end   // pulse came back
                        else if (countdown <= 1) begin state <= S_DISP; countdown <= 0; end
                        else countdown <= countdown - 1;
                    end
                end
                S_DISP: if (tick) state <= S_SIR;
                S_SIR:  if (ack_btn || cancel_btn) begin state <= S_MON; rearm <= REARM_S; end
                default: state <= S_MON;
            endcase

            // arming has priority over check-in
            if ((state == S_MON || state == S_CHK) && tick && arm_cond && rearm == 0
                && (arm_cnt + 1 >= ARM_HOLD_S)) begin
                state <= S_ARM; countdown <= CANCEL_S;
            end
        end
    end
endmodule
