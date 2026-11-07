@echo off
REM Bit-exact check of rtl_edge\rtl\edge_cnn_beat.sv against the Python integer model (serial, one xsim instance, own work folder xsim_work_c4).
REM 1) open a prompt and run  C:\AMDDesignTools\2025.2\Vivado\settings64.bat   2) cd into this folder   3) run_edge_vivado.bat [number_of_vectors, default 2064]
REM The parallel 12-chunk version used for the report is py\c4_run.py (same testbench).  Mutation check: python py\c4_run.py (builds modified COPIES under xsim_work_c4_mutsrc; no file under rtl\ is touched).
setlocal
set NV=%1
if "%NV%"=="" set NV=2064
if not exist xsim_work_c4 mkdir xsim_work_c4
cd xsim_work_c4
call xvlog -sv ..\rtl_edge\rtl\edge_cnn_beat.sv ..\rtl_edge\tb\tb_edge_cnn.sv || goto :err
call xelab work.tb_edge_cnn -s edge_snap --timescale 1ns/1ps -debug off > elab.log || goto :err
call xsim edge_snap -runall -testplusarg "VEC_START=0" -testplusarg "VEC_COUNT=%NV%" -testplusarg "OUT=c4_out_serial.txt" > ..\results\c4_rtl_serial_log.txt
findstr /C:"MISMATCH" /C:"passed" /C:"compute_cycles" ..\results\c4_rtl_serial_log.txt
exit /b 0
:err
echo *** A step failed. Send the first error lines above. ***
exit /b 1
