#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int read_int() {
    char buf[0x10];
    fgets(buf, sizeof(buf), stdin);
    return atoi(buf);
}

void print_flag() {
    char buf[0x100];
    FILE *f = fopen("flag.txt", "r");
    fread(buf, sizeof(buf), 1, f);
    puts(buf);
    exit(0);
}

void menu() {
    puts("JAG ÄR EN MENY");
}

void hax() {
    char buf[0x100];
    puts("Hur mycket vill du skriva?");
    int sz = read_int();
    read(0, buf, sz);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    menu();
    hax();
}
