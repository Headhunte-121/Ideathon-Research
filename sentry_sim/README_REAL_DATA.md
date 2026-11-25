# Real-data experiments (run on your PC)

Everything below uses recordings of real people from public datasets. Nothing here measures a cardiac arrest or ischemia
(no open dataset has that for this sensor set); it measures whether the device would FALSE ALARM or LOSE the heartbeat
on real signals. Do the steps in order. Each experiment is independent.

## 0. One-time setup (Command Prompt, same window every time)
    C:\AMDDesignTools\2025.2\Vivado\settings64.bat
    cd C:\College\Ideathon\sentry_sim_complete        (your project folder)
    pip install wfdb numpy scipy pandas matplotlib

## 1. Download the data (PhysioNet sets download themselves; sizes are approximate)
    python -c "import wfdb; wfdb.dl_database('nsrdb','real_data/nsrdb')"          (about 580 MB, 18 people, ~24 h each)
    python -c "import wfdb; wfdb.dl_database('nstdb','real_data/nstdb')"          (about 68 MB, real ECG + real motion/muscle noise)
    python -c "import wfdb; wfdb.dl_database('cebsdb','real_data/cebs',records=['b%03d'%i for i in range(1,21)])"   (20 people, real chest vibration SCG, 5 min each; NOTE the m### records are 50 min / ~2.4 GB each: do not download them)
PPG-DaLiA: download data.zip (2.7 GB, CC BY 4.0) from https://archive.ics.uci.edu/dataset/495/ppg+dalia , unzip into real_data\ppg_dalia
so that real_data\ppg_dalia\S1\S1.pkl ... S15\S15.pkl exist.

## 2. Run the experiments
E1  Beat detector under real noise (NSTDB: noise at 24, 18, 12, 6, 0 and -6 dB SNR)
    python py/real_batch.py ecg --dir real_data/nstdb --noisy --records 118e24 118e18 118e12 118e06 118e00 118e_6 119e24 119e18 119e12 119e06 119e00 119e_6
E2  Beat detector on 18 real clean recordings (30 min from the middle of each)
    python py/real_batch.py ecg --dir real_data/nsrdb --records all --start-min 60 --minutes 30
E3  Drift detector false check-ins over about 18 x 24 h of real heart rate  (the big one; takes some minutes)
    python py/real_batch.py drift --dir real_data/nsrdb --records all
E4  Does the chest heartbeat vibration of living people stay above the "chest still" threshold?  (no Verilog needed)
    python py/real_scg_cebs.py --dir real_data/cebs --records b001 b002 b003 b004 b005 b006 b007 b008 b009 b010 b011 b012 b013 b014 b015 b016 b017 b018 b019 b020 --mv-per-g <VALUE>
    <VALUE> = 660 (LIS344ALH datasheet, +/-2 g range, 3.3 V; use 220 as the lower bound for the +/-6 g range). The CEBS files do NOT document the conditioning gain; see results/REAL_DATA_REPORT.md section 3.5. Original note: the sensor sensitivity in the units of the CEBS signal. Take it from real_data\cebs\info.txt / README, the record header (.hea gain)
    and the LIS344ALH datasheet. Do NOT guess; a wrong value changes every number.
E5  Wrist pulse loss and motion in daily life  (no Verilog needed)
    python py/real_ppg_dalia.py --dir real_data/ppg_dalia --subjects 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
Add  --sim iverilog  to E1-E3 if you use Icarus instead of Vivado.
Results land in results\real_*.csv and are printed in the window. Send me those files (or paste the printed text).

## 3. How to read the results (my suggested pass marks: these are TARGETS, nothing more)
E1/E2  sensitivity and positive predictivity: clean >= 99%; noisy segments are expected to be worse, the table shows how much.
E3     false check-ins per 24 h per person: <= 1.  Any person with more is worth looking at (their heart rate may really drift).
E4     "% of living seconds below threshold": about 0 at the threshold you use. If a real person sits near it, the
       arrest check cannot separate "no heartbeat" from "healthy and still" and the threshold or the sensor must change.
E5     "pulse lost & still" in living people: should be near 0 for sitting; any large value there is the false-alarm risk.
