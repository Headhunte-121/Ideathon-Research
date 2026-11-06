`timescale 1ns/1ps
// SYSTEM END-TO-END TEST: patient model -> sensor-chip models -> Pod + Band + 5 BLE links + Phone.
// 1 simulated second = 1000 clocks (CLK_HZ=1000). Scenarios reset the whole device between runs.
// All body signals are our own simple models, NOT recordings.
module tb_system_end_to_end;
    localparam CLK_HZ = 1000;
    localparam S_MON = 0, S_CHK = 1, S_ARM = 2, S_DISP = 3, S_SIR = 4;
`ifdef MUT_A
    localparam PPT = 0;            // mutation A: wrist pulse check can never see a loss
`else
    localparam PPT = 1500;
`endif
`ifdef MUT_B
    localparam SCT = 65535;        // mutation B: chest always counted as "still"
`else
    localparam SCT = 5;
`endif
`ifdef ACCN
    localparam ACCNOISE = `ACCN;
`else
    localparam ACCNOISE = 350;
`endif
`ifdef BLE_LOSS
    localparam LOSS = `BLE_LOSS;
`else
    localparam LOSS = 0;
`endif

    reg clk = 0, rst_n = 0; always #1 clk = ~clk;
    // patient controls
    reg alive = 1, walking = 0, watch_loose = 0, ecg_off = 0, fall_trigger = 0, stress = 0;
    reg [11:0] hr_x10 = 12'd700;
    // environment
    reg button = 0, pb_up = 1, pp_up = 1, bph_up = 1, phone_on = 1;

    wire signed [31:0] ecg_uv, acc_ug, gyro_mdps, biz_mohm, ppg_na, gsr_ns, temp_mc, hs_au;
    body_physiology_model #(.CLK_HZ(CLK_HZ)) patient (.clk(clk), .alive(alive), .walking(walking), .watch_loose(watch_loose),
        .ecg_off(ecg_off), .fall_trigger(fall_trigger), .stress(stress), .hr_x10(hr_x10),
        .ecg_uv(ecg_uv), .chest_acc_ug(acc_ug), .gyro_mdps(gyro_mdps), .biz_mohm(biz_mohm), .ppg_na(ppg_na),
        .gsr_ns(gsr_ns), .temp_mc(temp_mc), .heart_sound_au(hs_au));

    wire siren, cpr, haptic, lnk_lost, canlock, call, gps, sms, callcan, drift, learned, fall, fresh, ploss, still, dacked;
    wire [2:0] st, ost; wire [5:0] cd, ocd; wire [31:0] call_t, ble_lost;
    wire [15:0] dpk, tpk, bpk, hr, se, me, bpp, hsnd, gsrl, dsent; wire [7:0] resp, dseq; wire [11:0] tc10;
    sentry_device_top #(.CLK_HZ(CLK_HZ), .PP_THR(PPT), .SCG_THR(SCT), .BLE_LOSS_PM(LOSS), .ACC_NOISE_UG(ACCNOISE), .COOL_S(20), .REARM_S(60)) dut (
        .clk(clk), .rst_n(rst_n), .ecg_uv(ecg_uv), .biz_mohm(biz_mohm), .chest_acc_ug(acc_ug), .gyro_mdps(gyro_mdps),
        .temp_mc(temp_mc), .heart_sound_au(hs_au), .ppg_na(ppg_na), .gsr_ns(gsr_ns),
        .button_raw(button), .pod_band_up(pb_up), .pod_phone_up(pp_up), .band_phone_up(bph_up), .phone_on(phone_on),
        .siren_en(siren), .cpr_beat(cpr), .band_haptic(haptic), .link_lost_band(lnk_lost),
        .pod_state(st), .pod_countdown(cd), .cancel_locked(canlock), .band_oled_state(ost), .band_oled_countdown(ocd),
        .call_placed(call), .gps_sent(gps), .sms_sent(sms), .call_cancelled(callcan), .call_time_clk(call_t),
        .dispatch_pkts(dpk), .telemetry_pkts(tpk), .band_pkts_at_phone(bpk),
        .hr_q4(hr), .scg_energy(se), .mov_energy(me), .band_ppg_pp(bpp),
        .drift_flag(drift), .learned(learned), .fall_flag(fall), .band_fresh(fresh), .pulse_loss(ploss), .chest_still(still),
        .resp_bpm(resp), .temp_c10(tc10), .heart_sound(hsnd), .gsr_level(gsrl),
        .disp_seq(dseq), .dispatch_acked(dacked), .dispatch_sent(dsent), .ble_lost_total(ble_lost));

    // ---------- bookkeeping ----------
    integer pass = 0, fail = 0, t0 = 0, now = 0, only = 0, t_callclk = -1;
    initial if (!$value$plusargs("ONLY=%d", only)) only = 0;
    always @(posedge call) t_callclk <= now;
`ifdef DBG
    always @(posedge clk) if (now % 1000 == 0 && now > 90000 && now < 100000) $display("t=%0d st=%0d cd=%0d hap=%b ploss=%b still=%b fall=%b fresh=%b se=%0d me=%0d bpp=%0d resp=%0d drift=%b dack=%b", now/1000, st, cd, haptic, ploss, still, fall, fresh, se, me, bpp, resp, drift, dacked, dut.u_pod.impact_seen, dut.u_pod.still_s, dut.u_pod.impact_age, call, siren);
`endif
    integer t_arm, t_disp, t_sir, t_call, n_haptic_clks, n_mon_exit;
    reg seen_arm, seen_chk, seen_disp, seen_sir;
    reg [2:0] pst = 0;
    always @(posedge clk) begin
        now <= now + 1;
        pst <= st;
        if (st != pst) begin
            if (st == S_CHK)  begin seen_chk <= 1; end
            if (st == S_ARM  && !seen_arm)  begin seen_arm  <= 1; t_arm  <= now; end
            if (st == S_DISP && !seen_disp) begin seen_disp <= 1; t_disp <= now; end
            if (st == S_SIR  && !seen_sir)  begin seen_sir  <= 1; t_sir  <= now; end
        end
    end
    task clear_marks; begin seen_arm = 0; seen_chk = 0; seen_disp = 0; seen_sir = 0; t_arm = -1; t_disp = -1; t_sir = -1; end endtask
    task check; input string msg; input cond;
        begin if (cond) begin pass = pass + 1; $display("  PASS  %0s", msg); end
              else begin fail = fail + 1; $display("  FAIL  %0s", msg); end end
    endtask
    task wait_s; input integer s; begin repeat (s * CLK_HZ) @(posedge clk); end endtask
    task do_reset;
        begin
            alive = 1; walking = 0; watch_loose = 0; ecg_off = 0; stress = 0; hr_x10 = 700; button = 0;
            pb_up = 1; pp_up = 1; bph_up = 1; phone_on = 1;
            rst_n = 0; repeat (20) @(posedge clk); rst_n = 1; clear_marks;
        end
    endtask
    task settle; begin wait_s(90); end endtask   // learning of the pulse trace, filters, first telemetry
    function integer secs; input integer clks; begin secs = clks / CLK_HZ; end endfunction

    initial begin
        $display("=== SYSTEM END-TO-END TEST (patient -> chips -> pod + band + BLE + phone) ===");

        // S1 normal rest
        if (only==0 || only==1) begin
        $display("S1: normal resting, 3 minutes");
        do_reset; settle; wait_s(90);
        check("S1 pod stays in MONITOR", st == S_MON && !seen_chk && !seen_arm);

        check("S1 no wrist buzz, no call, no siren", !haptic && !call && !siren);
        check("S1 heart rate near 70 bpm (from chest ECG)", hr > 16'd1000 && hr < 16'd1250);
        check("S1 band telemetry is reaching the pod", fresh);
        check("S1 phone receives telemetry from pod and band", tpk > 10 && bpk > 100);
        check("S1 breathing rate near 15 /min (from chest impedance)", resp >= 10 && resp <= 20);
        check("S1 skin temperature near 33.4 C (334 tenths)", tc10 > 320 && tc10 < 350);
        check("S1 rest drift baseline learned", learned);
        end

        // S2 walking
        if (only==0 || only==2) begin
        $display("S2: walking at 105 bpm for 60 s");
        do_reset; settle; walking = 1; hr_x10 = 1050; wait_s(60);
        check("S2 walking: no arming, no call, no siren", !seen_arm && !call && !siren);
        check("S2 motion detected by gyro", me > 300);
        walking = 0; hr_x10 = 700;
        end

        // S3 watch loose
        if (only==0 || only==3) begin
        $display("S3: wrist watch loose (no PPG) but the heart is fine, 60 s");
        do_reset; settle; watch_loose = 1; wait_s(60);
        check("S3 pulse-loss seen at the wrist", ploss);
        check("S3 chest still shows heartbeat -> NO arming", !seen_arm && !call && !siren);
        watch_loose = 0;
        end

        // S4 chest electrodes lifted
        if (only==0 || only==4) begin
        $display("S4: chest electrodes lifted off, 60 s");
        do_reset; settle; ecg_off = 1; wait_s(60);
        check("S4 wrist pulse healthy -> NO arming", !seen_arm && !call && !siren);
        ecg_off = 0;
        end

        // S5 cardiac arrest, nobody cancels
        if (only==0 || only==5) begin
        $display("S5: cardiac arrest, nobody cancels");
        do_reset; settle; alive = 0; t0 = now; wait_s(90);
        check("S5 arms after about 3 s of pulse loss + still chest", seen_arm && secs(t_arm - t0) >= 2 && secs(t_arm - t0) <= 8);
        check("S5 wrist buzzes during countdown", seen_arm);
        check("S5 dispatch after the 30 s countdown", seen_disp && secs(t_disp - t_arm) >= 29 && secs(t_disp - t_arm) <= 33);
        check("S5 siren starts", seen_sir && siren);
        check("S5 phone acknowledged the dispatch", dacked);
        check("S5 call placed, GPS and SMS sent", call && gps && sms);
        check("S5 call within 45 s of arrest", call && secs(t_callclk - t0) <= 45);
        $display("      timeline: armed +%0d s, dispatch +%0d s, siren +%0d s, call +%0d s", secs(t_arm-t0), secs(t_disp-t0), secs(t_sir-t0), secs(t_callclk-t0));
        end

        // S6 arrest then cancel (user fine)
        if (only==0 || only==6) begin
        $display("S6: arrest-like pulse loss, user holds cancel for 2 s during countdown");
        do_reset; settle; watch_loose = 1; ecg_off = 0; alive = 0; wait_s(8);
        check("S6 armed (countdown running)", st == S_ARM || seen_arm);
        alive = 1; watch_loose = 0;                // user is actually fine; heart back
        button = 1; wait_s(4); button = 0; wait_s(5);
        check("S6 back to MONITOR after cancel", st == S_MON);
        check("S6 no call, no siren", !call && !siren);
        end

        // S7 fall + collapse
        if (only==0 || only==7) begin
        $display("S7: fall (4.5 g impact) then arrest at the same moment");
        do_reset; settle; fall_trigger = 1; repeat (3) @(posedge clk); fall_trigger = 0; alive = 0; t0 = now; wait_s(30);
        check("S7 fall flag raised (impact then still)", seen_arm);
        check("S7 dispatch well before the 30 s countdown would finish", seen_disp && secs(t_disp - t0) < 20);
        check("S7 call placed", call);
        $display("      timeline: armed +%0d s, dispatch +%0d s", secs(t_arm-t0), secs(t_disp-t0));
        end

        // S8 pod-band link down during arrest
        if (only==0 || only==8) begin
        $display("S8: arrest while the band link is down");
        do_reset; settle; pb_up = 0; alive = 0; t0 = now; wait_s(90);
        check("S8 band marked stale", !fresh);
        check("S8 pod falls back to chest-ECG pulse check and still dispatches", seen_disp && call);
        check("S8 band reports link lost", lnk_lost);
        end

        // S9 phone off
        if (only==0 || only==9) begin
        $display("S9: arrest with the phone switched off");
        do_reset; settle; phone_on = 0; alive = 0; wait_s(70);
        check("S9 siren still sounds locally", seen_sir && siren);
        check("S9 pod keeps retrying (several dispatch sends, none acknowledged)", dsent >= 5 && !dacked && !call);
        phone_on = 1; wait_s(8);
        check("S9 phone returns -> acknowledged and call placed", dacked && call);
        end

        // S10 siren cancelled by bystander/user
        if (only==0 || only==10) begin
        $display("S10: siren running, user cancels with 2 s hold");
        do_reset; settle; alive = 0; wait_s(50);
        check("S10 siren on", siren);
        alive = 1; button = 1; wait_s(4); button = 0; wait_s(4);
        check("S10 siren stops, pod back to MONITOR", !siren && st == S_MON);
        end

        // S11 stress
        if (only==0 || only==11) begin
        $display("S11: sweating / stress, HR up to 100 bpm at rest, 60 s");
        do_reset; settle; stress = 1; hr_x10 = 1000; wait_s(60);
        check("S11 no call, no siren", !seen_arm && !call && !siren);
        stress = 0; hr_x10 = 700;

        end
        $display("=== %0d passed, %0d failed; BLE packets lost in last run: %0d ===", pass, fail, ble_lost);
        $finish;
    end
endmodule
