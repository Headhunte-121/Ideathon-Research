// Bit-exact check of edge_cnn_beat against the Python integer model (py/edge_int_model.py).  Plusargs (quoted by the runner):
//   VEC_IN=<hex file, 75 int8 per vector>  VEC_EXP=<text file, one signed score per vector>  VEC_START=<first vector>  VEC_COUNT=<n>  OUT=<per-vector result file>
`timescale 1ns/1ps
module tb_edge_cnn;
    reg clk = 0, rst_n = 0, start = 0, in_valid = 0; reg signed [7:0] in_data = 0;
    wire done, busy; wire signed [31:0] score; wire [31:0] cc;
    edge_cnn_beat dut (.clk(clk), .rst_n(rst_n), .start(start), .in_valid(in_valid), .in_data(in_data), .done(done), .busy(busy), .score(score), .compute_cycles(cc));
    always #5 clk = ~clk;
    reg [7:0] vin [0:154799];
    integer expv [0:2063];
    string f_in, f_exp, f_out; integer vstart, vcount, v, i, fd, fo, pass, fail, tot, cmin, cmax, first_bad, r;
    initial begin
        if (!$value$plusargs("VEC_IN=%s", f_in)) f_in = "../rtl_edge/tb/vectors_in.mem";
        if (!$value$plusargs("VEC_EXP=%s", f_exp)) f_exp = "../rtl_edge/tb/vectors_expected.txt";
        if (!$value$plusargs("VEC_START=%d", vstart)) vstart = 0;
        if (!$value$plusargs("VEC_COUNT=%d", vcount)) vcount = 2064;
        if (!$value$plusargs("OUT=%s", f_out)) f_out = "c4_out.txt";
        $readmemh(f_in, vin);
        fd = $fopen(f_exp, "r"); for (i = 0; i < 2064; i = i + 1) r = $fscanf(fd, "%d\n", expv[i]); $fclose(fd);
        fo = $fopen(f_out, "w"); pass = 0; fail = 0; cmin = 32'h7fffffff; cmax = 0; first_bad = -1;
        repeat (4) @(posedge clk); rst_n = 1; repeat (2) @(posedge clk);
        for (v = vstart; v < vstart + vcount; v = v + 1) begin
            @(posedge clk); start <= 1; @(posedge clk); start <= 0;
            for (i = 0; i < 75; i = i + 1) begin in_valid <= 1; in_data <= vin[v * 75 + i]; @(posedge clk); end
            in_valid <= 0; tot = 0;
            while (!done && tot < 200000) begin @(posedge clk); tot = tot + 1; end
            if (score === expv[v] && done) pass = pass + 1;
            else begin fail = fail + 1; if (first_bad < 0) begin first_bad = v; $display("FIRST MISMATCH: vector %0d expected %0d got %0d (done=%0d)", v, expv[v], score, done); end end
            if (cc < cmin) cmin = cc; if (cc > cmax) cmax = cc;
            $fdisplay(fo, "%0d %0d %0d %0d %0d", v, expv[v], score, (score === expv[v] && done) ? 1 : 0, cc);
        end
        $fclose(fo);
        $display("compute_cycles min %0d max %0d", cmin, cmax);
        $display("=== %0d passed, %0d failed ===", pass, fail);
        $finish;
    end
endmodule
