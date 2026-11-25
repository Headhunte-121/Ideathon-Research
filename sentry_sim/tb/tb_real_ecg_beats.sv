`timescale 1ns/1ps
// Feeds a REAL ECG recording (prepared by py/real_data_prepare.py) into the beat detector at 250 Hz
// and writes every detected beat (sample index, heart rate in bpm*16) to a file.
// Run:  +ECGFILE=data/ecg_16265.hex +NSAMP=450000 +OUT=data/det_16265.txt
module tb_real_ecg_beats;
    reg clk = 0, rst_n = 0, sample_en = 0;
    reg signed [15:0] ecg = 0;
    always #1 clk = ~clk;
    wire beat; wire [15:0] hr_q4;
    ecg_beat_detector #(.FS(250)) dut (.clk(clk), .rst_n(rst_n), .sample_en(sample_en), .ecg(ecg), .beat(beat), .hr_q4(hr_q4));

    reg [15:0] mem [0:3999999];
    reg [1023:0] fin, fout;
    integer nsamp = 0, i, fd, nbeats = 0, idx = 0;
    initial begin
        if (!$value$plusargs("ECGFILE=%s", fin))  begin $display("need +ECGFILE=..."); $finish; end
        if (!$value$plusargs("NSAMP=%d", nsamp))  begin $display("need +NSAMP=..."); $finish; end
        if (!$value$plusargs("OUT=%s", fout))     fout = "data/det.txt";
        $readmemh(fin, mem);
        fd = $fopen(fout, "w");
        repeat (4) @(posedge clk); rst_n = 1; repeat (2) @(posedge clk);
        for (i = 0; i < nsamp; i = i + 1) begin
            idx = i; ecg = mem[i];
            sample_en = 1; @(posedge clk); sample_en = 0; repeat (3) @(posedge clk);
        end
        repeat (4) @(posedge clk);
        $fclose(fd);
        $display("real ECG replay done: %0d samples, %0d beats detected -> %0s", nsamp, nbeats, fout);
        $finish;
    end
    always @(posedge clk) if (beat) begin nbeats = nbeats + 1; $fdisplay(fd, "%0d %0d", idx, hr_q4); end
endmodule
