`timescale 1ns/1ps
// BEHAVIOURAL MODEL of one direction of a Bluetooth LE link.
// Packets are delivered in order after one connection interval plus random jitter; each packet can be
// lost with probability LOSS_PM per thousand; when link_up falls, everything in flight is lost.
// NOT modelled: advertising, pairing, retransmission at the radio layer, throughput limits, interference.
module ble_link_model #(
    parameter CLK_HZ = 1000, CI_MS = 30, JIT_MS = 10, LOSS_PM = 0, SEED = 1, W = 64, DEPTH = 8
)(
    input  wire         clk, rst_n, link_up,
    input  wire         tx_valid,
    input  wire [W-1:0] tx_data,
    output reg          rx_valid,
    output reg  [W-1:0] rx_data,
    output reg  [31:0]  n_sent, n_lost, n_delivered
);
    localparam integer CI_CLK  = (CI_MS  * CLK_HZ) / 1000;
    localparam integer JIT_CLK = (JIT_MS * CLK_HZ) / 1000;
    reg [W-1:0] q_data [0:DEPTH-1];
    reg [31:0]  q_due  [0:DEPTH-1];
    integer head, tail, count, i;
    reg [31:0] now, lfsr, last_due, due_n;
    reg prev_up;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            head = 0; tail = 0; count = 0; now <= 0; lfsr <= 32'hACE1 ^ SEED; last_due = 0; prev_up <= 0;
            rx_valid <= 0; rx_data <= 0; n_sent <= 0; n_lost <= 0; n_delivered <= 0;
        end else begin
            now <= now + 1;
            lfsr <= {lfsr[30:0], lfsr[31] ^ lfsr[21] ^ lfsr[1] ^ lfsr[0]};
            rx_valid <= 0;
            prev_up <= link_up;
            if (prev_up && !link_up) begin                       // link dropped: lose everything in flight
                n_lost <= n_lost + count; head = 0; tail = 0; count = 0;
            end
            if (tx_valid) begin
                n_sent <= n_sent + 1;
                if (!link_up || count == DEPTH || ((lfsr % 1000) < LOSS_PM)) n_lost <= n_lost + 1;
                else begin
                    due_n = now + CI_CLK + ((JIT_CLK > 0) ? ((lfsr >> 8) % (JIT_CLK + 1)) : 0);
                    if (due_n < last_due) due_n = last_due;      // keep order
                    last_due = due_n;
                    q_data[tail] = tx_data; q_due[tail] = due_n;
                    tail = (tail + 1) % DEPTH; count = count + 1;
                end
            end
            if (count > 0 && now >= q_due[head]) begin
                rx_valid <= 1; rx_data <= q_data[head];
                head = (head + 1) % DEPTH; count = count - 1; n_delivered <= n_delivered + 1;
            end
        end
    end
endmodule
