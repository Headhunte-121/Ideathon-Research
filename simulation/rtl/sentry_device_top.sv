// WHOLE DEVICE, wired as the architecture diagram:
//   body signals -> sensor-chip models -> POD node  <==BLE==> BAND node  ; both <==BLE==> PHONE
// Everything left of the chip models is the "patient"; everything right is the device under test.
module sentry_device_top #(
    parameter CLK_HZ = 1000,
    parameter LOG2N = 6, WIN = 10, WIN_THR = 5, CONSEC = 3, K2X16 = 230,
    parameter PP_THR = 1500, SCG_THR = 5, MOV_THR = 300,
    parameter ARM_HOLD_S = 3, CANCEL_S = 30, COOL_S = 300, REARM_S = 60,
    parameter BLE_LOSS_PM = 0, GATE_EN = 1, ACC_NOISE_UG = 350
)(
    input  wire clk, rst_n,
    // patient (from body_physiology_model)
    input  wire signed [31:0] ecg_uv, biz_mohm, chest_acc_ug, gyro_mdps, temp_mc, heart_sound_au, ppg_na, gsr_ns,
    // user / environment
    input  wire button_raw, pod_band_up, pod_phone_up, band_phone_up, phone_on,
    // device outputs
    output wire siren_en, cpr_beat, band_haptic, link_lost_band,
    output wire [2:0] pod_state, output wire [5:0] pod_countdown, output wire cancel_locked,
    output wire [2:0] band_oled_state, output wire [5:0] band_oled_countdown,
    output wire call_placed, gps_sent, sms_sent, call_cancelled,
    output wire [31:0] call_time_clk,
    output wire [15:0] dispatch_pkts, telemetry_pkts, band_pkts_at_phone,
    // observation
    output wire [15:0] hr_q4, scg_energy, mov_energy, band_ppg_pp,
    output wire drift_flag, learned, fall_flag, band_fresh, pulse_loss, chest_still,
    output wire [7:0] resp_bpm, output wire [11:0] temp_c10, output wire [15:0] heart_sound, gsr_level,
    output wire [7:0] disp_seq, output wire dispatch_acked, output wire [15:0] dispatch_sent,
    output wire [31:0] ble_lost_total
);
    // ---- sensor chips ----
    wire signed [15:0] ecg_code, biz_code, acc_code, gyro_code, ppg_code, temp_code, mic_code; wire [15:0] gsr_code;
    wire ecg_drdy, imu_drdy, ppg_drdy, gsr_drdy, temp_drdy, mic_drdy;
    afe_ads1292r_model  #(.CLK_HZ(CLK_HZ)) u_ads (.clk(clk), .rst_n(rst_n), .ecg_uv(ecg_uv), .biz_mohm(biz_mohm), .ecg_code(ecg_code), .biz_code(biz_code), .drdy(ecg_drdy));
    afe_lsm6dsox_model  #(.CLK_HZ(CLK_HZ), .ACC_NOISE_UG_RMS(ACC_NOISE_UG)) u_imu (.clk(clk), .rst_n(rst_n), .chest_acc_ug(chest_acc_ug), .gyro_mdps(gyro_mdps), .acc_code(acc_code), .gyro_code(gyro_code), .drdy(imu_drdy));
    afe_tmp117_model    #(.CLK_HZ(CLK_HZ)) u_tmp (.clk(clk), .rst_n(rst_n), .temp_mc(temp_mc), .temp_code(temp_code), .drdy(temp_drdy));
    afe_sph0645_model   #(.CLK_HZ(CLK_HZ)) u_mic (.clk(clk), .rst_n(rst_n), .heart_sound_au(heart_sound_au), .mic_code(mic_code), .drdy(mic_drdy));
    afe_max86141_model  #(.CLK_HZ(CLK_HZ)) u_ppg (.clk(clk), .rst_n(rst_n), .ppg_na(ppg_na), .ppg_code(ppg_code), .drdy(ppg_drdy));
    afe_gsr_adc_model   #(.CLK_HZ(CLK_HZ)) u_gsr (.clk(clk), .rst_n(rst_n), .gsr_ns(gsr_ns), .gsr_code(gsr_code), .drdy(gsr_drdy));

    // ---- BLE links (separate per direction) ----
    wire pb_tx_v, bp_tx_v, pp_tx_v, phone_tx_v, bph_tx_v; wire [63:0] pb_tx_d, bp_tx_d, pp_tx_d, phone_tx_d, bph_tx_d;
    wire pb_rx_v, bp_rx_v, pp_rx_v, phone_rx_v, bph_rx_v; wire [63:0] pb_rx_d, bp_rx_d, pp_rx_d, phone_rx_d, bph_rx_d;
    wire [31:0] l1s,l1l,l1d,l2s,l2l,l2d,l3s,l3l,l3d,l4s,l4l,l4d,l5s,l5l,l5d;
    ble_link_model #(.CLK_HZ(CLK_HZ), .LOSS_PM(BLE_LOSS_PM), .SEED(11)) l_pod_band    (.clk(clk), .rst_n(rst_n), .link_up(pod_band_up),   .tx_valid(pb_tx_v),    .tx_data(pb_tx_d),    .rx_valid(pb_rx_v),    .rx_data(pb_rx_d),    .n_sent(l1s), .n_lost(l1l), .n_delivered(l1d));
    ble_link_model #(.CLK_HZ(CLK_HZ), .LOSS_PM(BLE_LOSS_PM), .SEED(22)) l_band_pod    (.clk(clk), .rst_n(rst_n), .link_up(pod_band_up),   .tx_valid(bp_tx_v),    .tx_data(bp_tx_d),    .rx_valid(bp_rx_v),    .rx_data(bp_rx_d),    .n_sent(l2s), .n_lost(l2l), .n_delivered(l2d));
    ble_link_model #(.CLK_HZ(CLK_HZ), .LOSS_PM(BLE_LOSS_PM), .SEED(33)) l_pod_phone   (.clk(clk), .rst_n(rst_n), .link_up(pod_phone_up),  .tx_valid(pp_tx_v),    .tx_data(pp_tx_d),    .rx_valid(pp_rx_v),    .rx_data(pp_rx_d),    .n_sent(l3s), .n_lost(l3l), .n_delivered(l3d));
    ble_link_model #(.CLK_HZ(CLK_HZ), .LOSS_PM(BLE_LOSS_PM), .SEED(44)) l_phone_pod   (.clk(clk), .rst_n(rst_n), .link_up(pod_phone_up),  .tx_valid(phone_tx_v), .tx_data(phone_tx_d), .rx_valid(phone_rx_v), .rx_data(phone_rx_d), .n_sent(l4s), .n_lost(l4l), .n_delivered(l4d));
    ble_link_model #(.CLK_HZ(CLK_HZ), .LOSS_PM(BLE_LOSS_PM), .SEED(55)) l_band_phone  (.clk(clk), .rst_n(rst_n), .link_up(band_phone_up), .tx_valid(bph_tx_v),    .tx_data(bph_tx_d),   .rx_valid(bph_rx_v),   .rx_data(bph_rx_d),   .n_sent(l5s), .n_lost(l5l), .n_delivered(l5d));
    assign ble_lost_total = l1l + l2l + l3l + l4l + l5l;

    // ---- pod ----
    pod_node #(.CLK_HZ(CLK_HZ), .LOG2N(LOG2N), .WIN(WIN), .WIN_THR(WIN_THR), .CONSEC(CONSEC), .K2X16(K2X16),
               .PP_THR(PP_THR), .SCG_THR(SCG_THR), .MOV_THR(MOV_THR), .GATE_EN(GATE_EN),
               .ARM_HOLD_S(ARM_HOLD_S), .CANCEL_S(CANCEL_S), .COOL_S(COOL_S), .REARM_S(REARM_S)) u_pod (
        .clk(clk), .rst_n(rst_n),
        .ecg_code(ecg_code), .biz_code(biz_code), .acc_code(acc_code), .gyro_code(gyro_code), .temp_code(temp_code), .mic_code(mic_code),
        .ecg_drdy(ecg_drdy), .imu_drdy(imu_drdy), .temp_drdy(temp_drdy), .mic_drdy(mic_drdy),
        .band_rx_valid(bp_rx_v), .band_rx_data(bp_rx_d), .band_tx_valid(pb_tx_v), .band_tx_data(pb_tx_d),
        .phone_tx_valid(pp_tx_v), .phone_tx_data(pp_tx_d), .phone_rx_valid(phone_rx_v), .phone_rx_data(phone_rx_d),
        .siren_en(siren_en), .cpr_beat(cpr_beat),
        .state_o(pod_state), .countdown_o(pod_countdown), .cancel_locked_o(cancel_locked),
        .hr_q4_o(hr_q4), .scg_energy_o(scg_energy), .mov_energy_o(mov_energy),
        .drift_flag_o(drift_flag), .learned_o(learned), .fall_flag_o(fall_flag), .band_fresh_o(band_fresh),
        .pulse_loss_o(pulse_loss), .chest_still_o(chest_still),
        .resp_bpm_o(resp_bpm), .temp_c10_o(temp_c10), .heart_sound_o(heart_sound), .gsr_level_o(gsr_level),
        .disp_seq_o(disp_seq), .dispatch_acked_o(dispatch_acked), .dispatch_sent_o(dispatch_sent));

    // ---- band ----
    band_node #(.CLK_HZ(CLK_HZ)) u_band (
        .clk(clk), .rst_n(rst_n), .ppg_code(ppg_code), .gsr_code(gsr_code), .ppg_drdy(ppg_drdy), .gsr_drdy(gsr_drdy),
        .button_raw(button_raw), .pod_rx_valid(pb_rx_v), .pod_rx_data(pb_rx_d),
        .pod_tx_valid(bp_tx_v), .pod_tx_data(bp_tx_d), .phone_tx_valid(bph_tx_v), .phone_tx_data(bph_tx_d),
        .haptic_motor(band_haptic), .oled_countdown(band_oled_countdown), .oled_state(band_oled_state),
        .oled_cancel_locked(), .link_lost(link_lost_band), .ppg_pp_o(band_ppg_pp), .gsr_level_o());

    // ---- phone ----
    phone_app_model #(.CLK_HZ(CLK_HZ)) u_phone (
        .clk(clk), .rst_n(rst_n), .phone_on(phone_on), .pod_rx_valid(pp_rx_v), .pod_rx_data(pp_rx_d),
        .band_rx_valid(bph_rx_v), .band_rx_data(bph_rx_d), .ack_tx_valid(phone_tx_v), .ack_tx_data(phone_tx_d),
        .call_placed(call_placed), .gps_sent(gps_sent), .sms_sent(sms_sent), .call_cancelled(call_cancelled),
        .call_time_clk(call_time_clk), .dispatch_pkts(dispatch_pkts), .telemetry_pkts(telemetry_pkts), .band_pkts(band_pkts_at_phone));
endmodule
