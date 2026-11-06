`timescale 1ns/1ps
// BEHAVIOURAL MODELS of the sensor chips: sampling rate, resolution, noise, saturation, data-ready strobe.
// NOT modelled: SPI / I2C / I2S wire protocols, register maps, startup time, filters inside the chips.
// Noise and scale numbers are our ASSUMPTIONS and must be checked against each datasheet.

// ADS1292R-like: chest ECG and chest impedance (breathing). 250 SPS.
module afe_ads1292r_model #(parameter CLK_HZ = 1000, SPS = 250, CODES_PER_UV = 16, ECG_NOISE_CODES = 20, BIZ_NOISE_MOHM = 15)(
    input  wire clk, rst_n,
    input  wire signed [31:0] ecg_uv, biz_mohm,
    output reg  signed [15:0] ecg_code, biz_code,
    output reg  drdy
);
    integer c = 0, seed = 11; real v;
    function integer sat16; input real x; begin sat16 = (x > 32767.0) ? 32767 : (x < -32768.0) ? -32768 : $rtoi(x); end endfunction
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin c <= 0; drdy <= 0; ecg_code <= 0; biz_code <= 0; end
        else begin
            drdy <= 0;
            c <= (c == CLK_HZ / SPS - 1) ? 0 : c + 1;
            if (c == 0) begin
                v = $itor(ecg_uv) * CODES_PER_UV + ECG_NOISE_CODES * 1.7 * (($random(seed) % 1000) / 1000.0);
                ecg_code <= sat16(v);
                v = $itor(biz_mohm - 30000) + BIZ_NOISE_MOHM * 1.7 * (($random(seed) % 1000) / 1000.0);
                biz_code <= sat16(v);
                drdy <= 1;
            end
        end
    end
endmodule

// LSM6DSOX-like IMU: chest accelerometer (one axis) and gyro. Accelerometer range +-4 g (122 ug/LSB), so an impact above 4 g saturates.
module afe_lsm6dsox_model #(parameter CLK_HZ = 1000, SPS = 250, ACC_LSB_UG = 122, ACC_NOISE_UG_RMS = 350, GYRO_LSB_MDPS = 9, GYRO_NOISE_MDPS_RMS = 40)(
    input  wire clk, rst_n,
    input  wire signed [31:0] chest_acc_ug, gyro_mdps,
    output reg  signed [15:0] acc_code, gyro_code,
    output reg  drdy
);
    integer c = 0, seed = 13; real v;
    function integer sat16; input real x; begin sat16 = (x > 32767.0) ? 32767 : (x < -32768.0) ? -32768 : $rtoi(x); end endfunction
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin c <= 0; drdy <= 0; acc_code <= 0; gyro_code <= 0; end
        else begin
            drdy <= 0;
            c <= (c == CLK_HZ / SPS - 1) ? 0 : c + 1;
            if (c == 0) begin
                v = ($itor(chest_acc_ug) + ACC_NOISE_UG_RMS * 1.732 * (($random(seed) % 1000) / 1000.0)) / ACC_LSB_UG;
                acc_code <= sat16(v);
                v = ($itor(gyro_mdps) + GYRO_NOISE_MDPS_RMS * 1.732 * (($random(seed) % 1000) / 1000.0)) / GYRO_LSB_MDPS;
                gyro_code <= sat16(v);
                drdy <= 1;
            end
        end
    end
endmodule

// MAX86141-like wrist PPG front end. 50 SPS, 1 nA per code, AC-coupled.
module afe_max86141_model #(parameter CLK_HZ = 1000, SPS = 50, NOISE_CODES = 20)(
    input  wire clk, rst_n,
    input  wire signed [31:0] ppg_na,
    output reg  signed [15:0] ppg_code,
    output reg  drdy
);
    integer c = 0, seed = 17; real v;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin c <= 0; drdy <= 0; ppg_code <= 0; end
        else begin
            drdy <= 0;
            c <= (c == CLK_HZ / SPS - 1) ? 0 : c + 1;
            if (c == 0) begin
                v = $itor(ppg_na) + NOISE_CODES * 1.7 * (($random(seed) % 1000) / 1000.0);
                ppg_code <= (v > 32767.0) ? 16'sd32767 : (v < -32768.0) ? -16'sd32768 : $rtoi(v);
                drdy <= 1;
            end
        end
    end
endmodule

// Palm GSR front end (a simple ADC on two pads). 10 SPS, 2 nS per code.
module afe_gsr_adc_model #(parameter CLK_HZ = 1000, SPS = 10)(
    input  wire clk, rst_n,
    input  wire signed [31:0] gsr_ns,
    output reg  [15:0] gsr_code,
    output reg  drdy
);
    integer c = 0;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin c <= 0; drdy <= 0; gsr_code <= 0; end
        else begin
            drdy <= 0;
            c <= (c == CLK_HZ / SPS - 1) ? 0 : c + 1;
            if (c == 0) begin gsr_code <= gsr_ns / 2; drdy <= 1; end
        end
    end
endmodule

// TMP117-like skin temperature sensor. 1 SPS, 7.8125 milli-deg C per code.
module afe_tmp117_model #(parameter CLK_HZ = 1000, SPS = 1)(
    input  wire clk, rst_n,
    input  wire signed [31:0] temp_mc,
    output reg  signed [15:0] temp_code,
    output reg  drdy
);
    integer c = 0;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin c <= 0; drdy <= 0; temp_code <= 0; end
        else begin
            drdy <= 0;
            c <= (c == CLK_HZ / SPS - 1) ? 0 : c + 1;
            if (c == 0) begin temp_code <= (temp_mc * 128) / 1000; drdy <= 1; end
        end
    end
endmodule

// SPH0645-like microphone, reduced to a 50 SPS heart-sound level (the real part streams I2S audio).
module afe_sph0645_model #(parameter CLK_HZ = 1000, SPS = 50, NOISE_CODES = 30)(
    input  wire clk, rst_n,
    input  wire signed [31:0] heart_sound_au,
    output reg  signed [15:0] mic_code,
    output reg  drdy
);
    integer c = 0, seed = 19; real v;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin c <= 0; drdy <= 0; mic_code <= 0; end
        else begin
            drdy <= 0;
            c <= (c == CLK_HZ / SPS - 1) ? 0 : c + 1;
            if (c == 0) begin
                v = $itor(heart_sound_au) + NOISE_CODES * 1.7 * (($random(seed) % 1000) / 1000.0);
                mic_code <= (v > 32767.0) ? 16'sd32767 : (v < -32768.0) ? -16'sd32768 : $rtoi(v);
                drdy <= 1;
            end
        end
    end
endmodule
