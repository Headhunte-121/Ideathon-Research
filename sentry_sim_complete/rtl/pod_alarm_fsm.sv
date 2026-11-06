// Alarm state machine of the Sentry Pod (follows the poster's state diagram, with the two-tier change):
//   MONITOR  -> CHECKIN : sustained baseline drift (wrist haptic nudge only, never a call)
//   MONITOR/CHECKIN -> ARMED : wrist pulse lost AND chest shows no heartbeat for ARM_HOLD_S  (30 s countdown on the band)
//   ARMED -> DISPATCH : countdown ends, OR a detected fall (impact over 3 g, then stillness)
//   DISPATCH -> SIREN : chest accelerometer confirms stillness (collapse); otherwise stand down
//   Cancel (2 s hold on the band, arrives as cancel_evt) works in ARMED unless locked after a fall; also ends CHECKIN and SIREN.
module pod_alarm_fsm #(
    parameter ARM_HOLD_S = 3, CANCEL_S = 30, CHECKIN_S = 60, COOL_S = 300, REARM_S = 60,
    parameter CLK_HZ = 1000
)(
    input  wire       clk, rst_n, tick,
    input  wire       drift_flag, pulse_loss, chest_still, fall_flag, cancel_evt,
    output wire [2:0] state_o,
    output reg  [5:0] countdown,
    output wire       haptic_cmd,          // wrist vibration requested
    output reg        cancel_locked,
    output wire       dispatch_req,        // level: keep telling the phone
    output wire       siren_en,
    output reg        cpr_beat,
    output reg        standdown_pulse      // one clock when a dispatch is called off
);
    localparam [2:0] S_MON = 0, S_CHK = 1, S_ARM = 2, S_DISP = 3, S_SIR = 4;
    localparam integer CPR_HALF = (CLK_HZ / 1000) * 272;      // 110 BPM
    reg [2:0]  state;
    reg [7:0]  arm_cnt, chk_cnt;
    reg [15:0] suppress, rearm;
    reg [31:0] cdiv;
    wire arm_cond = pulse_loss & chest_still;

    assign state_o      = state;
    assign haptic_cmd   = (state == S_CHK) || (state == S_ARM);
    assign dispatch_req = (state == S_DISP) || (state == S_SIR);
    assign siren_en     = (state == S_SIR);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= S_MON; arm_cnt <= 0; chk_cnt <= 0; suppress <= 0; rearm <= 0; countdown <= 0;
            cancel_locked <= 0; cpr_beat <= 0; cdiv <= 0; standdown_pulse <= 0;
        end else begin
            standdown_pulse <= 0;
            if (siren_en) begin
                if (cdiv >= CPR_HALF - 1) begin cdiv <= 0; cpr_beat <= ~cpr_beat; end else cdiv <= cdiv + 1;
            end else begin cdiv <= 0; cpr_beat <= 0; end

            if (tick) begin
                if (suppress != 0) suppress <= suppress - 1;
                if (rearm    != 0) rearm    <= rearm - 1;
                if ((state == S_MON || state == S_CHK) && arm_cond && rearm == 0) arm_cnt <= arm_cnt + 1;
                else arm_cnt <= 0;
            end

            case (state)
                S_MON: if (drift_flag && suppress == 0) begin state <= S_CHK; chk_cnt <= 0; end
                S_CHK: begin
                    if (cancel_evt) begin state <= S_MON; suppress <= COOL_S; end
                    else if (tick) begin
                        chk_cnt <= chk_cnt + 1;
                        if (chk_cnt + 1 >= CHECKIN_S) begin state <= S_MON; suppress <= COOL_S; end
                    end
                end
                S_ARM: begin
                    if (fall_flag) cancel_locked <= 1;
                    if (cancel_evt && !cancel_locked && !fall_flag) begin
                        state <= S_MON; rearm <= REARM_S; countdown <= 0; cancel_locked <= 0;
                    end else if (fall_flag) begin                     // impact then stillness: do not wait out the countdown
                        state <= S_DISP; countdown <= 0; cancel_locked <= 0;
                    end else if (tick) begin
                        if (!arm_cond) begin state <= S_MON; countdown <= 0; cancel_locked <= 0; end
                        else if (countdown <= 1) begin state <= S_DISP; countdown <= 0; cancel_locked <= 0; end
                        else countdown <= countdown - 1;
                    end
                end
                S_DISP: if (tick) begin
                    if (chest_still) state <= S_SIR;
                    else begin state <= S_MON; rearm <= REARM_S; standdown_pulse <= 1; end
                end
                S_SIR: if (cancel_evt) begin state <= S_MON; rearm <= REARM_S; standdown_pulse <= 1; end
                default: state <= S_MON;
            endcase

            if ((state == S_MON || state == S_CHK) && tick && arm_cond && rearm == 0 && (arm_cnt + 1 >= ARM_HOLD_S)) begin
                state <= S_ARM; countdown <= CANCEL_S; cancel_locked <= 0;
            end
        end
    end
endmodule
