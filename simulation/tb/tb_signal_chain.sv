`timescale 1ns/1ps
// END-TO-END virtual device test.
// Behavioural SENSOR MODELS (ECG, chest SCG, wrist PPG, motion reference) feed raw 250 Hz samples into
// the full RTL chain (NLMS -> beat detector -> drift detector / pulse check -> state machine).
// Two copies of the device see the same signals: dut_g has the rest-only gate, dut_n has it disabled.
// 1 simulated second = CLK_HZ clocks. All sensor waveforms are our own simple models, not recordings.
module tb_signal_chain;
    localparam CLK_HZ = 1000, FS = 250, SDIV = CLK_HZ / FS;
    localparam S_MON = 0, S_CHK = 1, S_ARM = 2, S_DISP = 3, S_SIR = 4;

    reg clk = 0, rst_n = 0, sample_en = 0;
    reg signed [15:0] ecg = 0, scg = 0, ppg = 0, mot = 0;
    reg cancel_btn = 0, ack_btn = 0, phone_link = 1, impact_g3 = 0;
    always #1 clk = ~clk;

    wire hap_g, call_g, sir_g, cpr_g, drift_g, lrn_g, beat_g;
    wire [5:0] cd_g; wire [2:0] st_g; wire [15:0] hr_g, pp_g, se_g, me_g;
    wire hap_n, call_n, sir_n, cpr_n, drift_n, lrn_n, beat_n;
    wire [5:0] cd_n; wire [2:0] st_n; wire [15:0] hr_n, pp_n, se_n, me_n;

    signal_chain_top #(.CLK_HZ(CLK_HZ), .FS(FS), .LOG2N(5), .WIN(8), .WIN_THR(4), .CONSEC(3),
                    .GATE_EN(1), .COOL_S(20), .REARM_S(60)) dut_g (
        .clk(clk), .rst_n(rst_n), .sample_en(sample_en), .ecg(ecg), .scg(scg), .ppg(ppg), .mot_ref(mot),
        .cancel_btn(cancel_btn), .ack_btn(ack_btn), .phone_link(phone_link), .impact_g3(impact_g3),
        .haptic(hap_g), .call_req(call_g), .siren_en(sir_g), .cpr_beat(cpr_g), .drift_flag(drift_g),
        .learned(lrn_g), .countdown(cd_g), .state_o(st_g), .hr_q4(hr_g), .ppg_pp(pp_g),
        .scg_energy(se_g), .mov_energy(me_g), .beat(beat_g));
    signal_chain_top #(.CLK_HZ(CLK_HZ), .FS(FS), .LOG2N(5), .WIN(8), .WIN_THR(4), .CONSEC(3),
                    .GATE_EN(0), .COOL_S(20), .REARM_S(60)) dut_n (
        .clk(clk), .rst_n(rst_n), .sample_en(sample_en), .ecg(ecg), .scg(scg), .ppg(ppg), .mot_ref(mot),
        .cancel_btn(cancel_btn), .ack_btn(ack_btn), .phone_link(phone_link), .impact_g3(impact_g3),
        .haptic(hap_n), .call_req(call_n), .siren_en(sir_n), .cpr_beat(cpr_n), .drift_flag(drift_n),
        .learned(lrn_n), .countdown(cd_n), .state_o(st_n), .hr_q4(hr_n), .ppg_pp(pp_n),
        .scg_energy(se_n), .mov_energy(me_n), .beat(beat_n));

    // ---------------- scenario controls (set by the test script) ----------------
    real    hr_target = 70.0;
    reg     alive = 1, walking = 0, watch_loose = 0, ecg_off = 0;

    // ---------------- sensor models ----------------
    real ts = 0.0, tb1 = -10.0, tb2 = -10.0, next_beat = 0.5;
    real rr = 0.0, rh0 = 0, rh1 = 0, rh2 = 0, rh3 = 0, rh4 = 0, rh5 = 0;
    real pi = 3.14159265358979;
    integer seed = 5, cnt = 0;

    function real u;               // uniform noise in (-1,1)
        input integer dummy;
        begin u = ($random(seed) % 1000) / 1000.0; end
    endfunction
    function real ecgw; input real dt;
        begin ecgw = 0.8 * $exp(-(dt / 0.012) * (dt / 0.012)) + 0.2 * $exp(-((dt - 0.25) / 0.05) * ((dt - 0.25) / 0.05)); end
    endfunction
    function real scgw; input real dt;
        begin scgw = (dt >= 0.0 && dt < 0.5) ? 0.25 * $exp(-dt / 0.07) * $sin(2.0 * pi * 20.0 * dt) : 0.0; end
    endfunction
    function real ppgw; input real dt;
        real x;
        begin
            x = (dt - 0.15) / 0.5;
            ppgw = (x > 0.0 && x < 1.0) ? 0.5 * $sin(pi * x) * $sin(pi * x) : 0.0;
        end
    endfunction

    real e_v, s_v, p_v, nzs;
    always @(posedge clk) begin
        cnt <= (cnt == SDIV - 1) ? 0 : cnt + 1;
        sample_en <= (cnt == 1);
        if (cnt == 0) begin
            ts = ts + 1.0 / FS;
            if (alive && ts >= next_beat) begin
                tb2 = tb1; tb1 = next_beat;
                next_beat = next_beat + 60.0 / hr_target + 0.03 * u(0);
            end
            // walking reference (2, 4, 6 Hz harmonics) and its history
            rr = (walking ? (0.30 * $sin(2.0*pi*2.0*ts) + 0.15 * $sin(2.0*pi*4.0*ts + 0.7) + 0.09 * $sin(2.0*pi*6.0*ts + 1.3)) : 0.0)
                 + 0.004 * u(0);
            rh5 = rh4; rh4 = rh3; rh3 = rh2; rh2 = rh1; rh1 = rh0; rh0 = rr;
            nzs = 0.9 * rh0 + 0.5 * rh2 - 0.3 * rh5;                   // unknown path from the body motion into the chest sensor
            // ECG
            e_v = ecgw(ts - tb1) + ecgw(ts - tb2) + 0.05 * $sin(2.0*pi*0.3*ts) + 0.01 * u(0) + 0.10 * rh1;
            if (ecg_off) e_v = 0.003 * u(0);
            // chest vibration
            s_v = scgw(ts - tb1) + scgw(ts - tb2) + nzs + 0.001 * u(0);
            // wrist PPG (heavily affected by arm motion)
            p_v = ppgw(ts - tb1) + ppgw(ts - tb2) + 0.4 * rh3 + 0.005 * u(0);
            if (watch_loose) p_v = 0.02 * u(0);
            ecg <= $rtoi(e_v * 16384.0); scg <= $rtoi(s_v * 16384.0);
            ppg <= $rtoi(p_v * 16384.0); mot <= $rtoi(rr * 16384.0);
        end
    end

    // ---------------- event monitors ----------------
    integer cyc = 0, t_arm = -1, t_call = -1, t0 = 0;
    reg seen_chk_g, seen_chk_n, seen_call_g, seen_call_n, seen_arm_g, seen_drift_n;
    always @(posedge clk) begin
        cyc <= cyc + 1;
        if (hap_g) seen_chk_g = 1;   if (hap_n) seen_chk_n = 1;
        if (call_g) seen_call_g = 1; if (call_n) seen_call_n = 1;
        if (drift_n) seen_drift_n = 1;
        if (st_g == S_ARM) begin seen_arm_g = 1; if (t_arm < 0) t_arm = cyc; end
        if (call_g && t_call < 0) t_call = cyc;
    end

    // ---------------- helpers ----------------
    integer pass = 0, fail = 0, k, edges;
    reg prev_cpr;
    task check(input cond, input string msg);
        begin
            if (cond) begin pass = pass + 1; $display("  PASS  %s", msg); end
            else      begin fail = fail + 1; $display("  FAIL  %s", msg); end
        end
    endtask
    task wait_s(input integer n); begin repeat (n * CLK_HZ) @(posedge clk); end endtask
    task press_cancel; begin cancel_btn = 1; repeat (5) @(posedge clk); cancel_btn = 0; end endtask
    task do_reset;
        begin
            rst_n = 0; alive = 1; walking = 0; watch_loose = 0; ecg_off = 0; hr_target = 70.0;
            cancel_btn = 0; ack_btn = 0; phone_link = 1;
            seen_chk_g = 0; seen_chk_n = 0; seen_call_g = 0; seen_call_n = 0; seen_arm_g = 0; seen_drift_n = 0;
            t_arm = -1; t_call = -1;
            next_beat = ts + 0.5; tb1 = ts - 10.0; tb2 = ts - 10.0;
            repeat (5) @(posedge clk); rst_n = 1; repeat (3) @(posedge clk);
        end
    endtask
    task rest_learn;
        begin wait_s(45); check(lrn_g, "baseline learned from 32 resting beats"); end
    endtask
    function real secs; input integer c; begin secs = c * 1.0 / CLK_HZ; end endfunction

    initial begin
        $display("=== END-TO-END virtual device test (raw 250 Hz sensor models -> full chain) ===");

        $display("E1 walking at 105 bpm after a resting baseline (rest-only gate vs no gate)");
        do_reset; rest_learn;
        walking = 1; hr_target = 105.0; wait_s(60);
        $display("   info: motion energy %0d, wrist pulse size %0d, chest energy %0d, last HR %0d bpm",
                 me_g, pp_g, se_g, hr_g / 16);
        check(!seen_chk_g && !seen_call_g && !seen_arm_g, "gated device: no check-in, no call while walking");
        check(seen_chk_n || seen_drift_n, "ablation: ungated device DOES raise a false drift check-in when walking");

        $display("E2 resting heart rate drifts from 70 to 100 bpm");
        do_reset; rest_learn;
        hr_target = 100.0; wait_s(90);
        check(seen_chk_g, "sustained resting drift gives a haptic check-in");
        check(!seen_call_g && !sir_g, "drift alone never calls or sounds the siren");

        $display("E3 cardiac arrest at rest (heart stops)");
        do_reset; rest_learn; wait_s(5);
        alive = 0; t0 = cyc; wait_s(60);
        $display("   timeline: arrest at t=%0.1f s, armed at +%0.1f s, call at +%0.1f s", secs(t0), secs(t_arm - t0), secs(t_call - t0));
        check(t_arm > 0 && secs(t_arm - t0) > 2.0 && secs(t_arm - t0) < 12.0, "armed within 2 to 12 s of the heart stopping");
        check(t_call > 0 && secs(t_call - t_arm) > 28.0 && secs(t_call - t_arm) < 32.0, "call requested about 30 s after arming");
        check(sir_g, "siren on");
        edges = 0; prev_cpr = cpr_g;
        repeat (2 * CLK_HZ) begin @(posedge clk); if (cpr_g !== prev_cpr) edges = edges + 1; prev_cpr = cpr_g; end
        check(edges >= 6 && edges <= 8, "CPR coach beating at 110 BPM");

        $display("E4 arrest detected, wearer cancels inside the window");
        do_reset; rest_learn; alive = 0;
        k = 0; while (st_g != S_ARM && k < 30 * CLK_HZ) begin @(posedge clk); k = k + 1; end
        check(st_g == S_ARM, "armed");
        wait_s(10); press_cancel; wait_s(45);
        check(!seen_call_g && st_g == S_MON, "cancel stops the call");

        $display("E5 walking with the watch loose (wrist pulse unreadable)");
        do_reset; rest_learn; walking = 1; watch_loose = 1; hr_target = 105.0; wait_s(40);
        $display("   info: chest energy %0d (threshold 40), wrist pulse size %0d", se_g, pp_g);
        check(!seen_arm_g && !seen_call_g, "heartbeat still seen in the chest (after noise cancelling): no false arming");

        $display("E6 resting with the watch off");
        do_reset; rest_learn; watch_loose = 1; wait_s(40);
        $display("   info: chest energy %0d", se_g);
        check(!seen_arm_g && !seen_call_g, "chest heartbeat vetoes a missing wrist pulse");

        $display("E7 chest electrode lifts off while alive");
        do_reset; rest_learn; ecg_off = 1; wait_s(40);
        check(!seen_arm_g && !seen_call_g, "wrist pulse vetoes a lost ECG");

        $display("=== %0d passed, %0d failed ===", pass, fail);
        if (fail == 0) $display("ALL TESTS PASSED"); else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
