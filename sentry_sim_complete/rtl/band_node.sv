// PULSEBAND (wrist, nRF52840 role).
//   PPG -> wrist pulse size once a second -> BLE telemetry to the pod (and to the phone)
//   GSR -> skin conductance level (context)
//   cancel button: a 2 s hold sends a cancel event (repeated 5 times, 200 ms apart, so one lost packet cannot lose a cancel)
//   commands from the pod -> vibration motor and OLED countdown; "link lost" if the pod is silent for LINK_LOST_S
module band_node #(parameter CLK_HZ = 1000, HOLD_S = 2, LINK_LOST_S = 5)(
    input  wire clk, rst_n,
    input  wire signed [15:0] ppg_code, input wire [15:0] gsr_code,
    input  wire ppg_drdy, gsr_drdy,
    input  wire button_raw,
    input  wire pod_rx_valid, input wire [63:0] pod_rx_data,
    output reg  pod_tx_valid, output reg [63:0] pod_tx_data,
    output reg  phone_tx_valid, output reg [63:0] phone_tx_data,
    output wire haptic_motor,
    output wire [5:0] oled_countdown,
    output wire [2:0] oled_state,
    output wire oled_cancel_locked,
    output wire link_lost,
    output reg  [15:0] ppg_pp_o, gsr_level_o
);
    reg [31:0] tdiv; wire tick = (tdiv == CLK_HZ - 1);
    always @(posedge clk or negedge rst_n) if (!rst_n) tdiv <= 0; else tdiv <= tick ? 0 : tdiv + 1;

    // PPG pulse size per second
    reg signed [15:0] mx, mn; reg signed [16:0] pp;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin mx <= -16'sd32768; mn <= 16'sd32767; ppg_pp_o <= 16'hFFFF; end
        else begin
            if (ppg_drdy) begin if (ppg_code > mx) mx <= ppg_code; if (ppg_code < mn) mn <= ppg_code; end
            if (tick) begin
                pp = mx - mn; ppg_pp_o <= (pp > 17'sd65535) ? 16'hFFFF : pp[15:0];
                mx <= -16'sd32768; mn <= 16'sd32767;
            end
        end
    end
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) gsr_level_o <= 0; else if (gsr_drdy) gsr_level_o <= gsr_code;
    end

    // button: 2 s hold
    reg [7:0] hold_cnt; reg fired; reg [2:0] burst_left; reg [31:0] bdiv; reg [7:0] seq;
    localparam integer BURST_CLK = CLK_HZ / 5;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin hold_cnt <= 0; fired <= 0; burst_left <= 0; bdiv <= 0; seq <= 0; pod_tx_valid <= 0; pod_tx_data <= 0;
                          phone_tx_valid <= 0; phone_tx_data <= 0; end
        else begin
            pod_tx_valid <= 0; phone_tx_valid <= 0;
            if (tick) begin
                if (button_raw) begin if (hold_cnt != 8'hFF) hold_cnt <= hold_cnt + 1; end else begin hold_cnt <= 0; fired <= 0; end
                if (button_raw && hold_cnt + 1 >= HOLD_S && !fired) begin fired <= 1; burst_left <= 5; bdiv <= 0; end
                // telemetry: wrist pulse size and skin conductance, to pod and phone
                seq <= seq + 1;
                pod_tx_valid <= 1;   pod_tx_data   <= {4'd1, seq, ppg_pp_o, gsr_level_o, 20'd0};
                phone_tx_valid <= 1; phone_tx_data <= {4'd1, seq, ppg_pp_o, gsr_level_o, 20'd0};
            end else if (burst_left != 0) begin
                if (bdiv >= BURST_CLK - 1) begin
                    bdiv <= 0; burst_left <= burst_left - 1; seq <= seq + 1;
                    pod_tx_valid <= 1; pod_tx_data <= {4'd2, seq, 52'd0};
                end else bdiv <= bdiv + 1;
            end
        end
    end

    // commands from the pod
    reg [7:0] cmd_age; reg [2:0] st_r; reg [5:0] cd_r; reg hap_r, lock_r;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin cmd_age <= 8'hFF; st_r <= 0; cd_r <= 0; hap_r <= 0; lock_r <= 0; end
        else begin
            if (tick && cmd_age != 8'hFF) cmd_age <= cmd_age + 1;
            if (pod_rx_valid && pod_rx_data[63:60] == 4'd1) begin
                st_r <= pod_rx_data[59:57]; cd_r <= pod_rx_data[56:51]; hap_r <= pod_rx_data[50]; lock_r <= pod_rx_data[49]; cmd_age <= 0;
            end
        end
    end
    assign link_lost          = (cmd_age >= LINK_LOST_S);
    assign haptic_motor       = hap_r && !link_lost;
    assign oled_countdown     = cd_r;
    assign oled_state         = st_r;
    assign oled_cancel_locked = lock_r;
endmodule
