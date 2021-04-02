#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void win() {
    char flag[1024];
    FILE *f = fopen("flag.txt", "r");
    fread(flag, 1024, 1, f);
    printf("%s\n", flag);
}

// https://gist.githubusercontent.com/maxcountryman/1699708/raw/746c13d0c1a85e33393c9cc268ff615528a67e5a/bf.c
void interpret(char* input) {
    unsigned char tape[1024] = {0};
    unsigned char* ptr = tape;

    char current_char;
    size_t i;
    size_t loop;

    for (i = 0; input[i] != 0; i++) {
        current_char = input[i];
        if (current_char == '>') {
            ++ptr;
        } else if (current_char == '<') {
            --ptr;
        } else if (current_char == '+') {
            ++*ptr;
        } else if (current_char == '-') {
            --*ptr;
        } else if (current_char == '.' ) {
            putchar(*ptr);
        } else if (current_char == ',') {
            *ptr = getchar();
        } else if (current_char == '[') {
            continue;
        } else if (current_char == ']' && *ptr) {
            loop = 1;
            while (loop > 0) {
                current_char = input[--i];
                if (current_char == '[') {
                    loop--;
                } else if (current_char == ']') {
                    loop++;
                }
            }
        }
    }
}

int main() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    
    char input[64];
    int choice = 5;
    while (1) {
        puts("[ BIG BRAIN ]");
        puts("1. run bf code");
        puts("2. hint");
        puts("3. exit");
        printf("> ");
        scanf("%d", &choice);
        getc(stdin);
        switch (choice) {
        case 1:
            fgets(input, 64, stdin);
            interpret(input);
            break;
        case 2:
	    puts("nixpix! Inte det här året.");
            //printf("win = %p\n", &win);
            break;
        case 3:
        default:
            return 0;
        }
    }
}
