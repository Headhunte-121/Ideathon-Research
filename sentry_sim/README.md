# Sentry virtual-device test (Vivado xsim)

What this is: the Sentry's decision logic written as hardware (Verilog) and tested in simulation. It is a
*virtual device*: no sensors, no battery, no body. It shows the logic behaves as designed.

Folders: rtl/ (the design), tb/ (the tests), py/ (helper scripts), results/ (logs from my own run).

| Test | File | Run top module | What it proves |
|---|---|---|---|
| Whole-device scenarios | tb/tb_system.sv | tb_system | 10 scenarios, 22 checks (drift only = check-in; pulse loss + still chest = 30 s window; cancel; phone out of range; ...) |
| Drift false-alarm rate | tb/tb_drift.sv | tb_drift | check-ins per 24 h at K = 3.0 / 3.8 / 4.5 sigma, and detection delay |
| Noise canceller | tb/tb_nlms.sv | tb_nlms | SNR gain of the 16-tap NLMS filter, written to results/nlms_out.csv |

## Run in Vivado (GUI)
1. File > Project > New. RTL project, any part (xc7a35tcpg236-1 is fine). Do not add constraints.
2. Add Sources > Add or create design sources: rtl/sentry_fsm.sv, rtl/drift_det.sv, rtl/sentry_top.sv, rtl/nlms16.sv.
3. Add Sources > Add or create simulation sources: tb/tb_system.sv, tb/tb_drift.sv, tb/tb_nlms.sv.
4. Settings > Simulation > Simulation top module name: tb_system (change to tb_drift or tb_nlms for the other tests).
5. Flow Navigator > Run Simulation > Run Behavioral Simulation. In the Tcl console type: run all
   The PASS/FAIL lines appear in the Tcl console. In the Wave window add the signals state_o, countdown, haptic,
   call_req, siren_en, cpr_beat (for the poster screenshot, zoom to the test T3 and T4 areas).
6. tb_nlms writes results/nlms_out.csv relative to the simulation folder. Create a folder named results inside
   <project>.sim/sim_1/behav/xsim first, or the file will not be written.
7. For tb_drift on real data: Settings > Simulation > xsim.simulate > More Options, add
   -testplusarg HRFILE=C:/full/path/data/hr_16265.hex -testplusarg NBEATS=<number printed by the python script>
   For a +25% shift test add -testplusarg INJECT=1 -testplusarg PCT=25

## Run from a terminal (Vivado command prompt, in this folder)
    xvlog -sv rtl/sentry_fsm.sv rtl/drift_det.sv rtl/sentry_top.sv tb/tb_system.sv
    xelab tb_system -s sys && xsim sys -runall

(The same for tb_drift and tb_nlms; tb_nlms also needs rtl/nlms16.sv.)

## Real data (needs internet on your PC)
    pip install wfdb numpy
    python py/make_rr_hex.py 16265        # writes data/hr_16265.hex, prints the +NBEATS number
Repeat for other MIT-BIH Normal Sinus Rhythm records (16272, 16273, 16420, ...) and add up the check-ins.

## After the NLMS test
    python py/ref_nlms.py results/nlms_out.csv

## Honest limits (put these on the poster)
- Inputs to the decision chain are summary features (heart rate per beat, wrist pulse size per second, chest
  vibration energy per second), not raw sensor streams.
- The noise-canceller test uses synthetic walking noise that is exactly a short filtered copy of the reference,
  so its gain is optimistic. Real walking will give less.
- Thresholds (200 for pulse size and chest energy, 3.8 sigma, 30 s, 3 s hold) are placeholders, not clinical values.
- Nothing here says the device detects ischemia. It shows the alarm logic is sound and the timing is right.
- My own run used Icarus Verilog, not xsim. If xsim complains about a line, copy the message back to me.
