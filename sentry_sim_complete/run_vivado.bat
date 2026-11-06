@echo off
REM Run all Sentry simulations with Vivado xsim from a Windows command prompt.
REM 1) open a prompt and run:  C:\Xilinx\Vivado\<version>\settings64.bat   (path depends on your install)
REM 2) cd into this folder and run:  run_vivado.bat
REM Not yet tested in xsim by the author -- if anything errors, send the first error lines.
setlocal enabledelayedexpansion
if not exist xsim_work mkdir xsim_work
cd xsim_work
if not exist results mkdir results

set SRC=
for %%f in (..\rtl\*.sv) do set SRC=!SRC! %%f
for %%f in (..\model\*.sv) do set SRC=!SRC! %%f
for %%f in (..\tb\*.sv) do set SRC=!SRC! %%f

echo === compiling ===
call xvlog -sv %SRC% || goto :err

for %%t in (tb_decision_logic tb_drift_false_alarms tb_noise_canceller tb_signal_chain) do (
  echo === running %%t ===
  call xelab work.%%t -s %%t_snap --timescale 1ns/1ps -debug off > elab_%%t.log || goto :err
  call xsim %%t_snap -runall > ..\results\vivado_%%t.txt
  findstr /C:"FAIL" /C:"passed" ..\results\vivado_%%t.txt
)

echo === running tb_system_end_to_end (takes a few minutes) ===
call xelab work.tb_system_end_to_end -s sys_snap --timescale 1ns/1ps -debug off > elab_sys.log || goto :err
call xsim sys_snap -runall > ..\results\vivado_system_end_to_end.txt
findstr /C:"FAIL" /C:"passed" ..\results\vivado_system_end_to_end.txt

echo === mutation A (must FAIL many checks) ===
call xvlog -sv -d MUT_A -work mut_a %SRC% >nul || goto :err
call xelab mut_a.tb_system_end_to_end -s mut_a_snap --timescale 1ns/1ps -debug off >nul || goto :err
call xsim mut_a_snap -runall | findstr /C:"passed"

echo === mutation B (must FAIL at least one check) ===
call xvlog -sv -d MUT_B -work mut_b %SRC% >nul || goto :err
call xelab mut_b.tb_system_end_to_end -s mut_b_snap --timescale 1ns/1ps -debug off >nul || goto :err
call xsim mut_b_snap -runall | findstr /C:"passed"

echo Done. Full logs are in the results folder (vivado_*.txt).
exit /b 0
:err
echo *** A step failed. Send the first error lines above. ***
exit /b 1
