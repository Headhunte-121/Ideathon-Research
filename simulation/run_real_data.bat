@echo off
REM Real-data test with Vivado xsim.  Usage:  run_real_data.bat 16265 [start_minute] [minutes]
REM Needs: settings64.bat already run in this window, Python with wfdb numpy scipy, and the record files
REM (<rec>.hea <rec>.dat <rec>.atr) in the folder  real_data\   next to this file.
setlocal
set REC=%1
set START=%2
set MINS=%3
if "%REC%"=="" (echo usage: run_real_data.bat 16265 [start_min] [minutes] & exit /b 1)
if "%START%"=="" set START=60
if "%MINS%"=="" set MINS=30
python py\real_data_prepare.py %REC% --dir real_data --start-min %START% --minutes %MINS% > data_prep_%REC%.txt || goto :err
type data_prep_%REC%.txt
for /f "tokens=3" %%a in ('findstr /C:"samples at 250 Hz" data_prep_%REC%.txt') do set NS=%%a
if not exist xsim_work mkdir xsim_work
cd xsim_work
call xvlog -sv ..\rtl\ecg_beat_detector.sv ..\rtl\baseline_drift_detector.sv ..\tb\tb_real_ecg_beats.sv ..\tb\tb_drift_false_alarms.sv >nul || goto :err
call xelab work.tb_real_ecg_beats -s real_snap --timescale 1ns/1ps -debug off >nul || goto :err
cd ..
xsim_work\xsim real_snap -runall -testplusarg ECGFILE=data/ecg_%REC%.hex -testplusarg NSAMP=%NS% -testplusarg OUT=data/det_%REC%.txt >nul
python py\real_data_score.py %REC% > results\real_beats_%REC%.txt
type results\real_beats_%REC%.txt
cd xsim_work
call xelab work.tb_drift_false_alarms -s drift_snap --timescale 1ns/1ps -debug off >nul || goto :err
for /f %%n in ('find /c /v "" ^< ..\data\hr_%REC%.hex') do set NB=%%n
call xsim drift_snap -runall -testplusarg HRFILE=../data/hr_%REC%.hex -testplusarg NBEATS=%NB% | findstr /C:"beats=" /C:"flags" /C:"per 24" > ..\results\real_drift_%REC%.txt
cd ..
type results\real_drift_%REC%.txt
exit /b 0
:err
echo *** a step failed. See the first error above. ***
exit /b 1
