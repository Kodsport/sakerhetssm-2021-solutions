#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

void print_flag() {
    char buf[0x100];
    FILE *f = fopen("flag.txt", "r");
    fread(buf, sizeof(buf), 1, f);
    puts(buf);
    exit(0);
}

size_t read_ulong() {
    size_t s;
    scanf("%lu", &s);
    return s;
}

unsigned int read_uint() {
    unsigned int c;
    scanf("%u", &c);
    while ( getchar() != '\n' );
    return c;
}

size_t prompt(char *text) {
    printf("%s", text);
    return read_ulong();
}

char *mmap_addr = 0;
void call_mmap() {
    size_t addr     = prompt("addr: ");
    size_t length   = prompt("length: ");
    size_t prot     = prompt("prot: ");
    size_t flags    = prompt("flags: ");
    size_t fd       = prompt("fd: ");
    size_t offset   = prompt("offset: ");

    mmap_addr = (char*)mmap((void *)addr, length, prot, flags, fd, offset);
    printf("%p\n", mmap_addr);
}

void write_mmap() {
    if (mmap_addr == 0) {
        puts("Kör mmap först!");
        return;
    }
    size_t sz = prompt("Hur mycket vill du skriva?");
    for(
        size_t total_read = 0, num_read;
        (num_read = read(STDIN_FILENO, &mmap_addr[total_read], sz - total_read)) > 0 && total_read < sz;
        total_read += num_read
    ) {
#ifdef DEBUG
        printf("Read: %lu+=%lu, %lu\n", total_read, num_read, sz);
#endif
    }
}

void print_mapping() {
    int fd = open("/proc/self/maps", O_RDONLY);
    if (fd < 0) {
        printf("fel fel fel! :(\n");
        exit(-1);
    }
    char c, s;
    while ((s = read(fd, &c, 1)) > 0) {
        printf("%c", c);
    }
}

void menu() {
    puts("1. mmap");
    puts("2. write");
    puts("3. /proc/self/maps");
    puts("4. exit");
    puts(">");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    int done = 0;
    while(!done) {
        menu();

        int c = read_uint();
        switch (c) {
            case 1:
                call_mmap();
            break;
            case 2:
                write_mmap();
            break;
            case 3:
                print_mapping();
            break;
            case 4:
                done = 1;
            break;
        }
    }
    return 0;
}
