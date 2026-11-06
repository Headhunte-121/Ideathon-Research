`timescale 1ns/1ps
// Walking-noise cancellation test on a SYNTHETIC chest signal (fs = 250 Hz).
// clean = SCG-like bursts at 1.2 Hz; noise = walking harmonics (2, 4, 6 Hz) reaching the chest
// through a short unknown filter; the reference r sees the walking motion directly.
// Writes results/noise_canceller_output.csv (clean, noisy, reference, rtl_out) for py/check_noise_canceller_vs_float.py.
module tb_noise_canceller;
    localparam FS = 250, N = 5000;
    reg clk = 0, rst_n = 0, in_valid = 0;
    reg signed [15:0] d = 0, r = 0;
    wire signed [15:0] e;
    wire out_valid;
    always #1 clk = ~clk;

    motion_noise_canceller #(.MU_SHIFT(2)) dut (.clk(clk), .rst_n(rst_n), .in_valid(in_valid), .d(d), .r(r),
                                .e_out(e), .out_valid(out_valid));

    real t, rr, beatphase, clean_r, nz_r, dr, rhist [0:7];
    integer n, fd, sd = 3, k;
    integer ci [0:N-1];
    real s_sig = 0, s_noise = 0, s_resid = 0, pi = 3.14159265358979;
    real snr_b, snr_a;
    integer cleanq;

    function real beatwave(input real tt);
        real ph;
        begin
            ph = tt * 1.2 - $floor(tt * 1.2);            // 0..1 within a beat
            beatwave = 0.25 * $exp(-ph * 14.0) * $sin(2.0 * pi * 20.0 * ph);
        end
    endfunction

    initial begin
        for (k = 0; k < 8; k = k + 1) rhist[k] = 0;
        fd = $fopen("results/noise_canceller_output.csv", "w");
        $fwrite(fd, "clean,noisy,ref,rtl\n");
        repeat (4) @(posedge clk); rst_n = 1; repeat (2) @(posedge clk);
        for (n = 0; n < N; n = n + 1) begin
            t = n * 1.0 / FS;
            rr = 0.30 * $sin(2.0*pi*2.0*t) + 0.15 * $sin(2.0*pi*4.0*t + 0.7) + 0.09 * $sin(2.0*pi*6.0*t + 1.3)
                 + 0.01 * ($itor($random(sd) % 100) / 100.0);
            for (k = 7; k > 0; k = k - 1) rhist[k] = rhist[k-1];
            rhist[0] = rr;
            nz_r    = 0.9 * rhist[0] + 0.5 * rhist[2] - 0.3 * rhist[5];   // unknown path to the chest
            clean_r = beatwave(t);
            d = $rtoi((clean_r + nz_r) * 32768.0 * 0.5);
            r = $rtoi(rr * 32768.0 * 0.5);
            in_valid = 1; @(posedge clk); in_valid = 0; @(posedge clk);
            // metrics on the last half, when the filter has converged
            if (n >= N / 2) begin
                dr = $itor(e) / 16384.0;                  // back to the same scale as clean_r
                s_sig   = s_sig   + clean_r * clean_r;
                s_noise = s_noise + nz_r * nz_r;
                s_resid = s_resid + (dr - clean_r) * (dr - clean_r);
            end
            $fwrite(fd, "%f,%f,%f,%f\n", clean_r, nz_r + clean_r, rr, $itor(e) / 16384.0);
        end
        $fclose(fd);
        snr_b = 10.0 * $log10(s_sig / s_noise);
        snr_a = 10.0 * $log10(s_sig / s_resid);
        $display("NLMS (synthetic walking noise, last half of %0d samples)", N);
        $display("SNR before: %.2f dB   SNR after: %.2f dB   gain: %.2f dB", snr_b, snr_a, snr_a - snr_b);
        if (snr_a > snr_b + 3.0) $display("PASS: gain above 3 dB"); else $display("FAIL: gain below 3 dB");
        $finish;
    end
endmodule
