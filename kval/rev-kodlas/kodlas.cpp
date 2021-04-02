#include <stdio.h>
#include <stdlib.h>
#include "Vkodlas.h"
#include "verilated.h"

int main(int argc, char** argv) {

    const int code[] = { 5, 6, 0, 3, 9, 2, 5, 0, 9, 4, 8, 2, 0, 5, 9 };
    /*const int row[] = { 3, 0, 0, 0, 1, 1, 1, 2, 2, 2 };
    const int col[] = { 1, 0, 1, 2, 0, 1, 2, 0, 1, 2 };*/

    Verilated::commandArgs(argc, argv);
    Vkodlas *tb = new Vkodlas;

    tb->COL_1 = 0;
    tb->COL_2 = 0;
    tb->COL_3 = 0;
    tb->CLK = 0;
    tb->RST = 0;
    tb->eval();
    tb->CLK = 1;
    tb->RST = 0;
    tb->eval();
    //printf("Row: %d%d%d%d, Lock: %d\n", tb->ROW_A, tb->ROW_B, tb->ROW_C, tb->ROW_D, tb->LOCK);
    
    for(size_t code_idx = 0; code_idx < 15; code_idx++) {
        printf("Digit: %d\n", code[code_idx]);
        tb->RST = 1;
        for(int i = 0; i < 20; i++) {
            switch(code[code_idx]) {
                case 0:
                    if(tb->ROW_D) tb->COL_2 = 1; else tb->COL_2 = 0;
                    break;
                case 1:
                    if(tb->ROW_A) tb->COL_1 = 1; else tb->COL_1 = 0;
                    break;
                case 2:
                    if(tb->ROW_A) tb->COL_2 = 1; else tb->COL_2 = 0;
                    break;
                case 3:
                    if(tb->ROW_A) tb->COL_3 = 1; else tb->COL_3 = 0;
                    break;
                case 4:
                    if(tb->ROW_B) tb->COL_1 = 1; else tb->COL_1 = 0;
                    break;
                case 5:
                    if(tb->ROW_B) tb->COL_2 = 1; else tb->COL_2 = 0;
                    break;
                case 6:
                    if(tb->ROW_B) tb->COL_3 = 1; else tb->COL_3 = 0;
                    break;
                case 7:
                    if(tb->ROW_C) tb->COL_1 = 1; else tb->COL_1 = 0;
                    break;
                case 8:
                    if(tb->ROW_C) tb->COL_2 = 1; else tb->COL_2 = 0;
                    break;
                case 9:
                    if(tb->ROW_C) tb->COL_3 = 1; else tb->COL_3 = 0;
                    break;
            }
            
            tb->CLK = 1 - tb->CLK;
            tb->eval();
            printf("CLK: %d, Row: %d%d%d%d (%d), Col: %d%d%d, Lock: %d, (%d, %d)\n", tb->CLK, tb->ROW_A, tb->ROW_B, tb->ROW_C, tb->ROW_D, tb->COL_1, tb->COL_2, tb->COL_3, tb->kodlas__DOT__keypad__DOT__row_select, tb->LOCK, tb->kodlas__DOT__key, tb->kodlas__DOT__lock_a__DOT__state);
        }
        printf("----\n");

        tb->COL_1 = 0;
        tb->COL_2 = 0;
        tb->COL_3 = 0;
        for(int i = 0; i < 20; i++) {
            tb->CLK = 1 - tb->CLK;
            tb->eval();
            printf("CLK: %d, Row: %d%d%d%d (%d), Col: %d%d%d, Lock: %d, (%d, %d)\n", tb->CLK, tb->ROW_A, tb->ROW_B, tb->ROW_C, tb->ROW_D, tb->COL_1, tb->COL_2, tb->COL_3, tb->kodlas__DOT__keypad__DOT__row_select, tb->LOCK, tb->kodlas__DOT__key, tb->kodlas__DOT__lock_a__DOT__state);
        }
    }
}
