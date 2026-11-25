`timescale 1ns/1ps
// Whole-device scenario test (virtual device). 1 "second" = CLK_HZ clocks.
module tb_decision_logic;
    localparam CLK_HZ = 1000;
    localparam S_MON = 0, S_CHK = 1, S_ARM = 2, S_DISP = 3, S_SIR = 4;

    reg clk = 0, rst_n = 0;
    reg beat_valid = 0;
    reg [15:0] hr_q4 = 0, ppg_pp = 16'd1000, scg_energy = 16'd1000;
    reg cancel_btn = 0, ack_btn = 0, phone_link = 1, impact_g3 = 0;
    wire haptic, call_req, siren_en, cpr_beat, drift_flag, learned;
    wire [5:0] countdown;
    wire [2:0] state_o;

    decision_chain_top #(.CLK_HZ(CLK_HZ), .LOG2N(6), .WIN(10), .WIN_THR(5), .CONSEC(3),
                 .K2X16(230), .COOL_S(20), .REARM_S(60)) dut (
        .clk(clk), .rst_n(rst_n), .beat_valid(beat_valid), .hr_q4(hr_q4),
        .ppg_pp(ppg_pp), .scg_energy(scg_energy), .cancel_btn(cancel_btn), .ack_btn(ack_btn),
        .phone_link(phone_link), .impact_g3(impact_g3), .haptic(haptic), .call_req(call_req),
        .siren_en(siren_en), .cpr_beat(cpr_beat), .drift_flag(drift_flag), .learned(learned),
        .countdown(countdown), .state_o(state_o));

    always #1 clk = ~clk;   // 2 time units per clock

    integer pass = 0, fail = 0, seed = 7;
    integer k, t, edges;
    reg seen_arm, seen_call, seen_chk;
    reg prev_cpr;

    task check(input cond, input string msg);
        begin
            if (cond) begin pass = pass + 1; $display("  PASS  %s", msg); end
            else      begin fail = fail + 1; $display("  FAIL  %s", msg); end
        end
    endtask

    task wait_s(input integer n);
        begin repeat (n * CLK_HZ) @(posedge clk); end
    endtask

    task do_reset;
        begin
            rst_n = 0; beat_valid = 0; cancel_btn = 0; ack_btn = 0; phone_link = 1;
            ppg_pp = 16'd1000; scg_energy = 16'd1000; impact_g3 = 0;
            repeat (5) @(posedge clk);
            rst_n = 1; repeat (3) @(posedge clk);
        end
    endtask

    task press_cancel; begin cancel_btn = 1; repeat (5) @(posedge clk); cancel_btn = 0; end endtask
    task press_ack;    begin ack_btn = 1;    repeat (5) @(posedge clk); ack_btn = 0;    end endtask

    // one heartbeat feature: centre bpm*16 plus noise (sum of two uniforms, about 2 bpm sd)
    task beat(input integer centre_q4);
        integer nz;
        begin
            nz = ($random(seed) % 41) + ($random(seed) % 41);
            hr_q4 = centre_q4 + nz;
            beat_valid = 1; @(posedge clk); beat_valid = 0;
            repeat (4) @(posedge clk);
        end
    endtask

    task feed(input integer n, input integer centre_q4);
        integer q;
        begin for (q = 0; q < n; q = q + 1) beat(centre_q4); end
    endtask

    task pulse_stops; begin ppg_pp = 0; scg_energy = 0; end endtask
    task pulse_back;  begin ppg_pp = 16'd1000; scg_energy = 16'd1000; end endtask

    initial begin
        $display("=== Sentry virtual-device test (1 s = %0d clocks) ===", CLK_HZ);

        // T1: a normal stretch must not raise any check-in
        $display("T1 normal heart rate, no false check-in");
        do_reset; seen_chk = 0;
        feed(64, 1120);                          // learn at 70 bpm
        check(learned, "baseline learned after 64 beats");
        for (k = 0; k < 200; k = k + 1) begin beat(1120); if (haptic) seen_chk = 1; end
        check(!seen_chk && !drift_flag && state_o == S_MON, "200 normal beats: no drift, no check-in");

        // T2: sustained drift gives a check-in only, never a call
        $display("T2 drift gives check-in only");
        do_reset; seen_call = 0; seen_chk = 0;
        feed(64, 1120);
        for (k = 0; k < 80; k = k + 1) begin
            beat(1520);                          // 95 bpm
            if (haptic) seen_chk = 1;
            if (call_req) seen_call = 1;
        end
        check(seen_chk && drift_flag, "sustained +25 bpm raises drift flag and haptic check-in");
        wait_s(5);
        check(!call_req && !siren_en, "no call or siren from drift alone");
        press_ack; repeat (4) @(posedge clk);
        check(state_o == S_MON && !haptic, "acknowledge returns to monitoring");

        // T3: pulse stops -> countdown -> dispatch -> siren + CPR beat
        $display("T3 pulse loss with still chest dispatches after 30 s");
        do_reset; pulse_stops;
        wait_s(4);
        check(state_o == S_ARM, "armed after about 3 s of pulse loss + still chest");
        t = 0;
        while (!call_req && t < 40 * CLK_HZ) begin @(posedge clk); t = t + 1; end
        check(t > 27 * CLK_HZ && t < 31 * CLK_HZ, "call requested about 30 s after arming");
        check(siren_en, "siren on");
        edges = 0; prev_cpr = cpr_beat;
        repeat (2 * CLK_HZ) begin @(posedge clk); if (cpr_beat !== prev_cpr) edges = edges + 1; prev_cpr = cpr_beat; end
        check(edges >= 6 && edges <= 8, "CPR beat toggles about 7 times in 2 s (110 BPM)");
        press_ack; repeat (4) @(posedge clk);
        check(state_o == S_MON && !siren_en, "acknowledge stops siren");

        // T4: cancel at 10 s
        $display("T4 cancel inside the window");
        do_reset; pulse_stops; seen_call = 0;
        wait_s(14);
        check(state_o == S_ARM, "armed");
        press_cancel; repeat (4) @(posedge clk);
        check(state_o == S_MON, "cancel returns to monitoring");
        for (k = 0; k < 40 * CLK_HZ; k = k + 1) begin @(posedge clk); if (call_req) seen_call = 1; end
        check(!seen_call, "no call after cancel (re-arm hold)");

        // T5: moving chest + low wrist signal (watch loose) must not arm
        $display("T5 moving chest with weak wrist signal does not arm");
        do_reset; ppg_pp = 0; scg_energy = 16'd1000; seen_arm = 0;
        for (k = 0; k < 15 * CLK_HZ; k = k + 1) begin @(posedge clk); if (state_o == S_ARM) seen_arm = 1; end
        check(!seen_arm, "never armed");

        // T6: phone out of range -> no call, but siren and CPR still run
        $display("T6 phone out of range");
        do_reset; phone_link = 0; pulse_stops; seen_call = 0;
        wait_s(36);
        for (k = 0; k < 3 * CLK_HZ; k = k + 1) begin @(posedge clk); if (call_req) seen_call = 1; end
        check(siren_en && !seen_call, "siren on, call_req stays low");
        edges = 0; prev_cpr = cpr_beat;
        repeat (2 * CLK_HZ) begin @(posedge clk); if (cpr_beat !== prev_cpr) edges = edges + 1; prev_cpr = cpr_beat; end
        check(edges >= 6 && edges <= 8, "CPR coach still beating");

        // T7: 2 s pulse dropout (below the 3 s hold) must not arm
        $display("T7 short dropout ignored");
        do_reset; seen_arm = 0; pulse_stops;
        for (k = 0; k < 2 * CLK_HZ; k = k + 1) begin @(posedge clk); if (state_o == S_ARM) seen_arm = 1; end
        pulse_back;
        for (k = 0; k < 6 * CLK_HZ; k = k + 1) begin @(posedge clk); if (state_o == S_ARM) seen_arm = 1; end
        check(!seen_arm && state_o == S_MON, "2 s dropout never arms");

        // T8: pulse returns during countdown
        $display("T8 pulse returns mid-countdown");
        do_reset; pulse_stops; seen_call = 0;
        wait_s(14);
        check(state_o == S_ARM, "armed");
        pulse_back;
        for (k = 0; k < 40 * CLK_HZ; k = k + 1) begin @(posedge clk); if (call_req) seen_call = 1; end
        check(state_o == S_MON && !seen_call, "returns to monitoring, no call");

        // T9: drift check-in is pre-empted by real pulse loss
        $display("T9 pulse loss during a check-in still arms");
        do_reset;
        feed(64, 1120); feed(60, 1520);
        check(state_o == S_CHK, "in check-in");
        pulse_stops; wait_s(5);
        check(state_o == S_ARM, "arming overrides check-in");

        // T10: sitting still with a good wrist pulse must not arm
        $display("T10 still chest but healthy pulse does not arm");
        do_reset; ppg_pp = 16'd1000; scg_energy = 0; seen_arm = 0;
        for (k = 0; k < 15 * CLK_HZ; k = k + 1) begin @(posedge clk); if (state_o == S_ARM) seen_arm = 1; end
        check(!seen_arm, "never armed when the pulse is present");

        $display("=== %0d passed, %0d failed ===", pass, fail);
        if (fail == 0) $display("ALL TESTS PASSED"); else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
