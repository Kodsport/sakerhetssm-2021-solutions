`default_nettype none

module kodlas(
    input wire CLK,
    input wire RST,

    input wire COL_1,
    input wire COL_2,
    input wire COL_3,

    output wire ROW_A,
    output wire ROW_B,
    output wire ROW_C,
    output wire ROW_D,

    output reg LOCK
);

    wire [3:0] key;

    keypad keypad(
        .clock(CLK),
        .reset(RST),
        .column1(COL_1),
        .column2(COL_2),
        .column3(COL_3),
        .row1(ROW_A),
        .row2(ROW_B),
        .row3(ROW_C),
        .row4(ROW_D),
        .key(key)
    );

    lock lock_a(
        .clock(CLK),
        .reset(RST),
        .key(key),
        .lock(LOCK)
    );

endmodule


/* verilator lint_off DECLFILENAME */
module keypad(
    input wire clock,
    input wire reset,

    input wire column1,
    input wire column2,
    input wire column3,

    output wire row1,
    output wire row2,
    output wire row3,
    output wire row4,

    output reg [3:0] key
);

    reg [3:0] scan_key;
    wire [1:0] row_select;
    assign row1 = row_select == 0;
    assign row2 = row_select == 1;
    assign row3 = row_select == 2;
    assign row4 = row_select == 3;

    mod_n_counter counter(
        .clock(clock),
        .reset(reset),
        .out(row_select)
    );

    always @ (posedge clock) begin
        if(!reset)
            key <= 0;
        else begin
            case(row_select)
                0: begin
                    key <= scan_key;
                    if(column1)
                        scan_key <= 12;
                    else if(column2)
                        scan_key <= 10;
                    else if(column3)
                        scan_key <= 1;
                    else
                        scan_key <= 0;
                end
                1: begin 
                    if(column1)
                        scan_key <= 8;
                    else if(column2)
                        scan_key <= 5;
                    else if(column3)
                        scan_key <= 4;
                end
                2: begin 
                    if(column1)
                        scan_key <= 7;
                    else if(column2)
                        scan_key <= 2;
                    else if(column3)
                        scan_key <= 11;
                end
                3: begin 
                    if(column1)
                        scan_key <= 3;
                    else if(column2)
                        scan_key <= 6;
                    else if(column3)
                        scan_key <= 9;
                end
            endcase
        end
    end
endmodule
/* verilator lint_on DECLFILENAME */

/* verilator lint_off DECLFILENAME */
module lock(
    input wire clock,
    input wire reset,
    input wire [3:0] key,
    output wire lock
);

    reg [3:0] prev_key;
    reg [3:0] state;
    assign lock = state == 15;

    always @ (posedge clock) begin
        if(!reset) begin
            state <= 0;
        end else if(prev_key != key) begin
            prev_key <= key;
            if(key != 0) begin
                case(state)
                0: if(key == 5) state <= 1; else state <= 0;
                1: if(key == 4) state <= 2; else state <= 0;
                2: if(key == 6) state <= 3; else state <= 0;
                3: if(key == 1) state <= 4; else state <= 0;
                4: if(key == 11) state <= 5; else state <= 0;
                5: if(key == 10) state <= 6; else state <= 0;
                6: if(key == 5) state <= 7; else state <= 0;
                7: if(key == 6) state <= 8; else state <= 0;
                8: if(key == 11) state <= 9; else state <= 0;
                9: if(key == 8) state <= 10; else state <= 0;
                10: if(key == 2) state <= 11; else state <= 0;
                11: if(key == 10) state <= 12; else state <= 0;
                12: if(key == 6) state <= 13; else state <= 0;
                13: if(key == 5) state <= 14; else state <= 0;
                14: if(key == 11) state <= 15; else state <= 0;
                endcase
            end
        end
    end

endmodule
/* verilator lint_on DECLFILENAME */

/* verilator lint_off DECLFILENAME */
module mod_n_counter #(
    parameter N = 3 /*4-1*/,
    parameter WIDTH = 2
)(
    input   clock,
    input   reset,
    output  reg[WIDTH-1:0] out
);  
  
  always @ (posedge clock) begin
    if (!reset) begin
      out <= 0;
    end else begin
      if (out == N)
        out <= 0;
      else
        out <= out + 1;
    end
  end
endmodule
/* verilator lint_on DECLFILENAME */
