`timescale 1ns/1ps
// BEHAVIOURAL MODEL of the phone app: acknowledges dispatch packets, then (after CALL_SETUP_S) sends GPS,
// calls 112 and texts the contacts. A stand-down that arrives before the call is placed cancels it.
// NOT modelled: the real phone OS, cell network, GPS accuracy, call connection time, user interaction.
module phone_app_model #(parameter CLK_HZ = 1000, CALL_SETUP_S = 2)(
    input  wire clk, rst_n, phone_on,
    input  wire pod_rx_valid, input wire [63:0] pod_rx_data,
    input  wire band_rx_valid, input wire [63:0] band_rx_data,
    output reg  ack_tx_valid, output reg [63:0] ack_tx_data,
    output reg  call_placed, gps_sent, sms_sent, call_cancelled,
    output reg  [31:0] call_time_clk, output reg [15:0] dispatch_pkts, telemetry_pkts, band_pkts
);
    reg [31:0] now, setup_cnt; reg pending; reg [7:0] cur_seq;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            now <= 0; setup_cnt <= 0; pending <= 0; cur_seq <= 0; ack_tx_valid <= 0; ack_tx_data <= 0;
            call_placed <= 0; gps_sent <= 0; sms_sent <= 0; call_cancelled <= 0; call_time_clk <= 0;
            dispatch_pkts <= 0; telemetry_pkts <= 0; band_pkts <= 0;
        end else begin
            now <= now + 1; ack_tx_valid <= 0;
            if (band_rx_valid) band_pkts <= band_pkts + 1;
            if (phone_on && pod_rx_valid) begin
                case (pod_rx_data[63:60])
                    4'd1: telemetry_pkts <= telemetry_pkts + 1;
                    4'd2: begin                                         // dispatch request
                        dispatch_pkts <= dispatch_pkts + 1;
                        ack_tx_valid <= 1; ack_tx_data <= {4'd3, pod_rx_data[59:52], 52'd0};
                        if (!pending && !call_placed && !(cur_seq == pod_rx_data[59:52] && call_cancelled)) begin
                            pending <= 1; setup_cnt <= 0; cur_seq <= pod_rx_data[59:52]; call_cancelled <= 0;
                        end
                    end
                    4'd4: if (pending && !call_placed) begin pending <= 0; call_cancelled <= 1; end   // stand-down
                    default: ;
                endcase
            end
            if (pending) begin
                setup_cnt <= setup_cnt + 1;
                if (setup_cnt >= CALL_SETUP_S * CLK_HZ) begin
                    pending <= 0; call_placed <= 1; gps_sent <= 1; sms_sent <= 1; call_time_clk <= now;
                end
            end
        end
    end
endmodule
