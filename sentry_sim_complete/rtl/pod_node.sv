// SENTRY POD (lower sternum, nRF5340 role). Everything the pod does, as hardware-style blocks.
// Inputs are the chip outputs (codes + data-ready) and BLE packets; outputs are the siren, CPR beat and BLE packets.
//   chest accel + gyro -> noise canceller -> chest heartbeat strength
//   ecg -> beat detector -> heart rate -> (rest-only gate) -> baseline drift detector
//   biz -> breathing rate;  temp, mic, GSR (from band) -> context values sent to the phone
//   impact (> 3 g) then stillness -> fall flag
//   band telemetry (wrist pulse size) over BLE -> pulse check; if the band goes silent: fall back to "no ECG beats for 6 s"
//   -> alarm state machine -> commands to band, dispatch packets (retried until the phone acknowledges) to phone
module pod_node #(
    parameter CLK_HZ = 1000, LOG2N = 11, WIN = 60, WIN_THR = 30, CONSEC = 5, K2X16 = 230,
    parameter PP_THR = 1500, SCG_THR = 5, MOV_THR = 300, IMPACT_CODE = 24590,
    parameter BAND_STALE_S = 5, NOBEAT_S = 6, FALL_STILL_S = 2, GATE_EN = 1,
    parameter ARM_HOLD_S = 3, CANCEL_S = 30, COOL_S = 300, REARM_S = 60, DISP_RETRY_S = 2
)(
    input  wire clk, rst_n,
    input  wire signed [15:0] ecg_code, biz_code, acc_code, gyro_code, temp_code, mic_code,
    input  wire ecg_drdy, imu_drdy, temp_drdy, mic_drdy,
    input  wire        band_rx_valid,  input wire [63:0] band_rx_data,    // from band
    output reg         band_tx_valid,  output reg [63:0] band_tx_data,    // to band
    output reg         phone_tx_valid, output reg [63:0] phone_tx_data,   // to phone
    input  wire        phone_rx_valid, input wire [63:0] phone_rx_data,   // from phone (acks)
    output wire        siren_en, cpr_beat,
    // observation points
    output wire [2:0]  state_o, output wire [5:0] countdown_o, output wire cancel_locked_o,
    output wire [15:0] hr_q4_o, scg_energy_o, mov_energy_o,
    output wire        drift_flag_o, learned_o, fall_flag_o, band_fresh_o, pulse_loss_o, chest_still_o,
    output reg  [7:0]  resp_bpm_o, output reg [11:0] temp_c10_o, output reg [15:0] heart_sound_o, output reg [15:0] gsr_level_o,
    output reg  [7:0]  disp_seq_o, output reg dispatch_acked_o, output reg [15:0] dispatch_sent_o
);
    // ---------- 1 Hz tick ----------
    reg [31:0] tdiv;
    wire tick = (tdiv == CLK_HZ - 1);
    always @(posedge clk or negedge rst_n) if (!rst_n) tdiv <= 0; else tdiv <= tick ? 0 : tdiv + 1;

    // ---------- chest signal chain ----------
    wire signed [15:0] scg_clean; wire scg_valid;
    motion_noise_canceller #(.MU_SHIFT(2)) u_nlms (.clk(clk), .rst_n(rst_n), .in_valid(imu_drdy),
        .d(acc_code), .r(gyro_code), .e_out(scg_clean), .out_valid(scg_valid));

    wire beat; wire [15:0] hr_q4;
    ecg_beat_detector #(.FS(250)) u_beat (.clk(clk), .rst_n(rst_n), .sample_en(ecg_drdy), .ecg(ecg_code), .beat(beat), .hr_q4(hr_q4));

    // 1-second summaries: chest heartbeat strength (cleaned), body motion (gyro), mic level
    reg [31:0] sum_s, sum_g, sum_m; reg [15:0] n_s, n_g, n_m;
    reg [15:0] scg_energy, mov_energy, heart_sound;
    wire [15:0] a_s = scg_clean[15] ? (~scg_clean + 1'b1) : scg_clean;
    wire [15:0] a_g = gyro_code[15] ? (~gyro_code + 1'b1) : gyro_code;
    wire [15:0] a_m = mic_code[15]  ? (~mic_code + 1'b1)  : mic_code;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sum_s <= 0; sum_g <= 0; sum_m <= 0; n_s <= 0; n_g <= 0; n_m <= 0;
            scg_energy <= 16'hFFFF; mov_energy <= 0; heart_sound <= 0;
        end else begin
            if (scg_valid) begin sum_s <= sum_s + a_s; n_s <= n_s + 1; end
            if (imu_drdy)  begin sum_g <= sum_g + a_g; n_g <= n_g + 1; end
            if (mic_drdy)  begin sum_m <= sum_m + a_m; n_m <= n_m + 1; end
            if (tick) begin
                if (n_s != 0) scg_energy  <= sum_s / n_s;
                if (n_g != 0) mov_energy  <= sum_g / n_g;
                if (n_m != 0) heart_sound <= sum_m / n_m;
                sum_s <= 0; sum_g <= 0; sum_m <= 0; n_s <= 0; n_g <= 0; n_m <= 0;
            end
        end
    end
    wire moving      = (mov_energy > MOV_THR);
    wire chest_still = (scg_energy < SCG_THR);

    // ---------- drift detector (rest-only baseline) ----------
    wire plausible = (hr_q4 >= 16'd480) && (hr_q4 <= 16'd3200);
    wire beat_ok   = beat && plausible && (GATE_EN ? !moving : 1'b1);
    wire drift_flag, learned;
    baseline_drift_detector #(.LOG2N(LOG2N), .WIN(WIN), .WIN_THR(WIN_THR), .CONSEC(CONSEC), .K2X16(K2X16)) u_drift (
        .clk(clk), .rst_n(rst_n), .beat_valid(beat_ok), .hr_q4(hr_q4), .learned(learned), .drift_flag(drift_flag));

    // ---------- fall detector: impact above 3 g, then stillness ----------
    wire signed [15:0] acc_abs_s = acc_code[15] ? -acc_code : acc_code;
    reg [7:0] impact_age, still_s, fall_hold; reg impact_seen, fall_flag;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin impact_seen <= 0; impact_age <= 0; still_s <= 0; fall_flag <= 0; fall_hold <= 0; end
        else begin
            if (imu_drdy && acc_abs_s >= IMPACT_CODE) begin impact_seen <= 1; impact_age <= 0; still_s <= 0; end
            if (tick) begin
                if (impact_seen) begin
                    impact_age <= impact_age + 1;
                    if (!moving) still_s <= still_s + 1; else still_s <= 0;
                    if (still_s + 1 >= FALL_STILL_S && !moving) begin fall_flag <= 1; fall_hold <= 60; impact_seen <= 0; end
                    else if (impact_age >= 10) impact_seen <= 0;
                end
                if (fall_hold != 0) begin fall_hold <= fall_hold - 1; if (fall_hold == 1) fall_flag <= 0; end
            end
        end
    end

    // ---------- breathing rate from chest impedance (zero crossings of a detrended trace, 30 s windows) ----------
    reg signed [31:0] zmean; reg signed [31:0] zd; reg zpos; reg [7:0] crossings; reg [5:0] rwin;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin zmean <= 0; zpos <= 0; crossings <= 0; rwin <= 0; resp_bpm_o <= 0; end
        else begin
            if (ecg_drdy) begin
                zd = ({{16{biz_code[15]}}, biz_code} <<< 4) - zmean;
                zmean <= zmean + (zd >>> 11);
                if (!zpos && zd > 2000) begin zpos <= 1; crossings <= crossings + 1; end
                else if (zpos && zd < -2000) zpos <= 0;
            end
            if (tick) begin
                if (rwin == 29) begin resp_bpm_o <= crossings * 2; crossings <= 0; rwin <= 0; end else rwin <= rwin + 1;
            end
        end
    end

    // ---------- temperature (code * 5 / 64 = tenths of a deg C) ----------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) temp_c10_o <= 0; else if (temp_drdy) temp_c10_o <= (temp_code * 5) / 64;
    end

    // ---------- band telemetry over BLE ----------
    reg [7:0] band_age; reg [15:0] band_ppg_pp; reg cancel_evt;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin band_age <= 8'hFF; band_ppg_pp <= 16'hFFFF; cancel_evt <= 0; gsr_level_o <= 0; end
        else begin
            cancel_evt <= 0;
            if (tick && band_age != 8'hFF) band_age <= band_age + 1;
            if (band_rx_valid) begin
                case (band_rx_data[63:60])
                    4'd1: begin band_ppg_pp <= band_rx_data[51:36]; gsr_level_o <= band_rx_data[35:20]; band_age <= 0; end
                    4'd2: cancel_evt <= 1;
                    default: ;
                endcase
            end
        end
    end
    wire band_fresh = (band_age < BAND_STALE_S);

    // seconds since the last ECG beat (fallback pulse check when the band is silent)
    reg [7:0] nobeat_s;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) nobeat_s <= 0;
        else if (beat) nobeat_s <= 0;
        else if (tick && nobeat_s != 8'hFF) nobeat_s <= nobeat_s + 1;
    end
    wire pulse_loss = band_fresh ? (band_ppg_pp < PP_THR) : (nobeat_s >= NOBEAT_S);

    // ---------- state machine ----------
    wire [2:0] state; wire [5:0] countdown; wire haptic_cmd, cancel_locked, dispatch_req, standdown_pulse;
    pod_alarm_fsm #(.CLK_HZ(CLK_HZ), .ARM_HOLD_S(ARM_HOLD_S), .CANCEL_S(CANCEL_S), .COOL_S(COOL_S), .REARM_S(REARM_S)) u_fsm (
        .clk(clk), .rst_n(rst_n), .tick(tick), .drift_flag(drift_flag), .pulse_loss(pulse_loss), .chest_still(chest_still),
        .fall_flag(fall_flag), .cancel_evt(cancel_evt), .state_o(state), .countdown(countdown), .haptic_cmd(haptic_cmd),
        .cancel_locked(cancel_locked), .dispatch_req(dispatch_req), .siren_en(siren_en), .cpr_beat(cpr_beat),
        .standdown_pulse(standdown_pulse));

    // ---------- BLE senders ----------
    reg [7:0] seq_b, seq_p; reg [2:0] pstate; reg dreq_d; reg [3:0] retry_cnt; reg [2:0] sd_left; reg [2:0] tel_cnt;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            band_tx_valid <= 0; phone_tx_valid <= 0; band_tx_data <= 0; phone_tx_data <= 0;
            seq_b <= 0; seq_p <= 0; pstate <= 0; dreq_d <= 0; retry_cnt <= 0; sd_left <= 0; tel_cnt <= 0;
            disp_seq_o <= 0; dispatch_acked_o <= 0; dispatch_sent_o <= 0;
        end else begin
            band_tx_valid <= 0; phone_tx_valid <= 0;
            pstate <= state; dreq_d <= dispatch_req;
            // command to the band: on a state change and every second
            if (tick || state != pstate) begin
                band_tx_valid <= 1; seq_b <= seq_b + 1;
                band_tx_data  <= {4'd1, state, countdown, haptic_cmd, cancel_locked, seq_b, 41'd0};
            end
            // phone acknowledges the current dispatch
            if (phone_rx_valid && phone_rx_data[63:60] == 4'd3 && phone_rx_data[59:52] == disp_seq_o) dispatch_acked_o <= 1;
            // dispatch: send on entry, then retry every DISP_RETRY_S until acknowledged
            if (dispatch_req && !dreq_d) begin
                disp_seq_o <= disp_seq_o + 1; dispatch_acked_o <= 0; retry_cnt <= 0; sd_left <= 0;
                phone_tx_valid <= 1; dispatch_sent_o <= dispatch_sent_o + 1;
                phone_tx_data <= {4'd2, disp_seq_o + 8'd1, state, 49'd0};
            end else if (dispatch_req && tick && !dispatch_acked_o) begin
                if (retry_cnt + 1 >= DISP_RETRY_S) begin
                    retry_cnt <= 0; phone_tx_valid <= 1; dispatch_sent_o <= dispatch_sent_o + 1;
                    phone_tx_data <= {4'd2, disp_seq_o, state, 49'd0};
                end else retry_cnt <= retry_cnt + 1;
            end else if (standdown_pulse) sd_left <= 3;
            else if (sd_left != 0 && tick) begin                              // stand-down, repeated 3 times
                sd_left <= sd_left - 1; phone_tx_valid <= 1; phone_tx_data <= {4'd4, disp_seq_o, 52'd0};
            end else if (tick) begin                                           // telemetry every 5 s
                tel_cnt <= (tel_cnt == 4) ? 0 : tel_cnt + 1;
                if (tel_cnt == 4) begin
                    phone_tx_valid <= 1; seq_p <= seq_p + 1;
                    phone_tx_data <= {4'd1, seq_p, hr_q4, resp_bpm_o, temp_c10_o, heart_sound};
                end
            end
        end
    end

    assign state_o = state; assign countdown_o = countdown; assign cancel_locked_o = cancel_locked;
    assign hr_q4_o = hr_q4; assign scg_energy_o = scg_energy; assign mov_energy_o = mov_energy;
    assign drift_flag_o = drift_flag; assign learned_o = learned; assign fall_flag_o = fall_flag;
    assign band_fresh_o = band_fresh; assign pulse_loss_o = pulse_loss; assign chest_still_o = chest_still;
    always @(*) heart_sound_o = heart_sound;
endmodule
