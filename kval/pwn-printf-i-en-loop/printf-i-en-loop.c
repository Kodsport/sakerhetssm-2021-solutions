#include <stdio.h>
#include <stdlib.h>

void print_flag() {
    char buf[0x100];
    FILE *f = fopen("flag.txt", "r");
    fread(buf, sizeof(buf), 1, f);
    puts(buf);
    exit(0);
}

int main() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);

    for (;;) {
        char buf[0x100];
        fgets(buf, sizeof(buf), stdin);
        printf(buf);
    }

    return 0;
}
