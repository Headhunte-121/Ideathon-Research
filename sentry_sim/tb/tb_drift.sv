`timescale 1ns/1ps
`ifndef ADAPT
`define ADAPT 10
`endif
// False check-in rate of the drift detector at K = 3.0, 3.8, 4.5 sigma.
// Default: synthetic heart rate. With +HRFILE=data/hr_16265.hex (+NBEATS=n) it replays a real recording
// made by py/make_rr_hex.py (values are bpm*16, one per line).
// With +INJECT=1 a +PCT% (default 25) heart-rate shift is added in the last quarter of the data and the delay is reported.
module tb_drift;
    localparam LOG2N = 13;           // learn on the first 8192 beats (about 2 hours)
    reg clk = 0, rst_n = 0, beat_valid = 0;
    reg [15:0] hr = 0;
    always #1 clk = ~clk;

    wire l30, l38, l45, f30, f38, f45;
    drift_det #(.LOG2N(LOG2N), .K2X16(144), .ADAPT_SHIFT(`ADAPT)) d30 (clk, rst_n, beat_valid, hr, l30, f30);
    drift_det #(.LOG2N(LOG2N), .K2X16(230), .ADAPT_SHIFT(`ADAPT)) d38 (clk, rst_n, beat_valid, hr, l38, f38);
    drift_det #(.LOG2N(LOG2N), .K2X16(324), .ADAPT_SHIFT(`ADAPT)) d45 (clk, rst_n, beat_valid, hr, l45, f45);

    reg [15:0] mem [0:399999];
    integer pct = 25, nbeats = 40000, i, seed = 11, nz, inject = 0, from_file = 0;
    integer r30 = 0, r38 = 0, r45 = 0, inj_at, first38 = -1, first30 = -1, first45 = -1;
    reg p30 = 0, p38 = 0, p45 = 0;
    reg [1023:0] fname;
    real sumhr = 0, hours;

    initial begin
        if ($value$plusargs("NBEATS=%d", nbeats)) ;
        if ($value$plusargs("INJECT=%d", inject)) ;
        if ($value$plusargs("PCT=%d", pct)) ;
        if ($value$plusargs("HRFILE=%s", fname)) begin from_file = 1; $readmemh(fname, mem); end
        inj_at = nbeats * 3 / 4;
        repeat (4) @(posedge clk); rst_n = 1; repeat (2) @(posedge clk);
        for (i = 0; i < nbeats; i = i + 1) begin
            if (from_file) hr = mem[i];
            else begin
                nz = ($random(seed) % 41) + ($random(seed) % 41) + ($random(seed) % 41);
                hr = 1120 + nz;                        // 70 bpm, about 2.5 bpm sd (synthetic)
            end
            if (inject && i >= inj_at) hr = hr + (hr * pct) / 100;
            sumhr = sumhr + hr;
            beat_valid = 1; @(posedge clk); beat_valid = 0; @(posedge clk);
            if (f30 && !p30) begin r30 = r30 + 1; if (i >= inj_at && first30 < 0) first30 = i - inj_at; end
            if (f38 && !p38) begin r38 = r38 + 1; if (i >= inj_at && first38 < 0) first38 = i - inj_at; end
            if (f45 && !p45) begin r45 = r45 + 1; if (i >= inj_at && first45 < 0) first45 = i - inj_at; end
            p30 = f30; p38 = f38; p45 = f45;
        end
        hours = nbeats / ((sumhr / nbeats) / 16.0 * 60.0);
        $display("beats=%0d  about %.1f hours of data  source=%s", nbeats, hours, from_file ? "file" : "synthetic");
        $display("flags raised (check-ins):  K=3.0: %0d   K=3.8: %0d   K=4.5: %0d", r30, r38, r45);
        $display("per 24 h:                  K=3.0: %.2f  K=3.8: %.2f  K=4.5: %.2f",
                 r30 * 24.0 / hours, r38 * 24.0 / hours, r45 * 24.0 / hours);
        if (inject) $display("beats from injected +%0d%% shift to first flag: K=3.0: %0d  K=3.8: %0d  K=4.5: %0d (-1 = missed)", pct, first30, first38, first45);
        $finish;
    end
endmodule
