`timescale 1ns/1ps
// BEHAVIOURAL MODEL of the wearer's body (not hardware). Produces physical signals in integer units
// from simple waveform models WE wrote (not recordings). Everything the sensors would see:
//   ecg_uv         chest ECG, microvolts           chest_acc_ug   chest accelerometer, micro-g (heartbeat vibration + body motion + impacts)
//   gyro_mdps      chest gyro, milli-deg/s         biz_mohm       chest impedance, milli-ohm (breathing)
//   ppg_na         wrist PPG, nanoamp (AC)         gsr_ns         palm skin conductance, nanosiemens
//   temp_mc        skin temperature, milli-deg C   heart_sound_au heart sounds, arbitrary units
module body_physiology_model #(parameter CLK_HZ = 1000, parameter FS = 250)(
    input  wire        clk,
    input  wire        alive,         // 0 = cardiac arrest (no heartbeats from now on)
    input  wire        walking,
    input  wire        watch_loose,   // wrist PPG has no skin contact
    input  wire        ecg_off,       // chest electrodes lifted off
    input  wire        fall_trigger,  // 1-clock pulse: body hits the ground
    input  wire        stress,        // sweating (GSR up)
    input  wire [11:0] hr_x10,        // heart rate in bpm * 10
    output reg  signed [31:0] ecg_uv, chest_acc_ug, gyro_mdps, biz_mohm, ppg_na, gsr_ns, temp_mc, heart_sound_au
);
    localparam SDIV = CLK_HZ / FS;
    real pi = 3.14159265358979;
    real ts = 0.0, tb1 = -10.0, tb2 = -10.0, next_beat = 0.5, t_fall = -10.0;
    real rr, rh0 = 0, rh1 = 0, rh2 = 0, rh3 = 0, rh4 = 0, rh5 = 0, nzs;
    real e_v, s_v, p_v, h_v, imp;
    integer cnt = 0, seed = 5;

    function real u; input integer dummy; begin u = ($random(seed) % 1000) / 1000.0; end endfunction
    function real ecgw; input real dt;
        begin ecgw = 0.8 * $exp(-(dt / 0.012) * (dt / 0.012)) + 0.2 * $exp(-((dt - 0.25) / 0.05) * ((dt - 0.25) / 0.05)); end
    endfunction
    function real scgw; input real dt;
        begin scgw = (dt >= 0.0 && dt < 0.5) ? 0.25 * $exp(-dt / 0.07) * $sin(2.0 * pi * 20.0 * dt) : 0.0; end
    endfunction
    function real ppgw; input real dt; real x;
        begin x = (dt - 0.15) / 0.5; ppgw = (x > 0.0 && x < 1.0) ? 0.5 * $sin(pi * x) * $sin(pi * x) : 0.0; end
    endfunction
    function real hsw; input real dt;     // S1 at the beat, S2 0.3 s later (half size)
        real a, b;
        begin
            a = (dt >= 0.0 && dt < 0.15) ? $exp(-dt / 0.03) * $sin(2.0 * pi * 60.0 * dt) : 0.0;
            b = (dt >= 0.3 && dt < 0.45) ? 0.5 * $exp(-(dt - 0.3) / 0.03) * $sin(2.0 * pi * 80.0 * (dt - 0.3)) : 0.0;
            hsw = a + b;
        end
    endfunction

    always @(posedge clk) begin
        if (fall_trigger) t_fall = ts;
        cnt <= (cnt == SDIV - 1) ? 0 : cnt + 1;
        if (cnt == 0) begin
            ts = ts + 1.0 / FS;
            if (alive && ts >= next_beat) begin
                tb2 = tb1; tb1 = next_beat;
                next_beat = next_beat + 600.0 / hr_x10 + 0.03 * u(0);
            end
            rr = (walking ? (0.30 * $sin(2.0*pi*2.0*ts) + 0.15 * $sin(2.0*pi*4.0*ts + 0.7) + 0.09 * $sin(2.0*pi*6.0*ts + 1.3)) : 0.0)
                 + 0.004 * u(0);
            rh5 = rh4; rh4 = rh3; rh3 = rh2; rh2 = rh1; rh1 = rh0; rh0 = rr;
            nzs = 0.9 * rh0 + 0.5 * rh2 - 0.3 * rh5;
            imp = (ts - t_fall >= 0.0 && ts - t_fall < 0.06) ? 4.5 * $sin(pi * (ts - t_fall) / 0.06) : 0.0;   // g

            e_v = (ecgw(ts - tb1) + ecgw(ts - tb2) + 0.05 * $sin(2.0*pi*0.3*ts) + 0.008 * u(0) + 0.10 * rh1) * 1250.0;
            if (ecg_off) e_v = 2.0 * u(0);
            s_v = (scgw(ts - tb1) + scgw(ts - tb2)) * 80000.0 + nzs * 600000.0 + imp * 1000000.0;
            p_v = (ppgw(ts - tb1) + ppgw(ts - tb2) + 0.4 * rh3 + 0.005 * u(0)) * 16384.0;
            if (watch_loose) p_v = 0.02 * u(0) * 16384.0;
            h_v = (hsw(ts - tb1) + hsw(ts - tb2)) * 8000.0;

            ecg_uv         <= $rtoi(e_v);
            chest_acc_ug   <= $rtoi(s_v);
            gyro_mdps      <= $rtoi(rr * 100000.0);
            biz_mohm       <= $rtoi(30000.0 + 400.0 * $sin(2.0 * pi * 0.25 * ts));
            ppg_na         <= $rtoi(p_v);
            gsr_ns         <= $rtoi(2000.0 + (stress ? 1500.0 : 0.0) + 10.0 * u(0));
            temp_mc        <= $rtoi(33400.0 + 10.0 * u(0));
            heart_sound_au <= $rtoi(h_v);
        end
    end
endmodule
