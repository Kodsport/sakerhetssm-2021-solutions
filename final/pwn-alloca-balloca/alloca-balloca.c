#include <stdio.h>
#include <alloca.h>
#include <unistd.h>
#include <stdlib.h>

#define N_CHUNKS 8

struct chunk {
    size_t size;
    void *buf;
};

struct chunk chunks[N_CHUNKS];

size_t read_ulong() {
    size_t s;
    scanf("%lu", &s);
    return s;
}

unsigned int read_uint() {
    unsigned int c;
    scanf("%u", &c);
    return c;
}

void read_buf(char *buf, size_t sz) {
    char c = 0;
    for (size_t i = 0; i < sz; i++) {
        read(0, &c, 1);
        if (c == '\n')
            break;
        buf[i] = c;
    }
}

void print_flag() {
    char buf[0x100];
    FILE *f = fopen("flag.txt", "r");
    fread(buf, sizeof(buf), 1, f);
    puts(buf);
    exit(0);
}

void menu() {
    puts("1. alloca");
    puts("2. read");
    puts("3. write");
    puts("4. delete");
    puts("5. exit");
    puts(">");
}

void alloc_chunk() {
    puts("Index:");
    unsigned int idx = read_uint();
    if (idx >= N_CHUNKS) {
        puts("aja baja!");
        return;
    }

    puts("Storlek:");
    size_t sz = read_ulong();

    void *buf = alloca(sz);
    chunks[idx].size = sz;
    chunks[idx].buf  = buf;
}

void read_chunk() {
    puts("Index:");
    unsigned int idx = read_uint();
    if (idx >= N_CHUNKS) {
        puts("aja baja!");
        return;
    }

    write(1, chunks[idx].buf, chunks[idx].size);
}

void write_chunk() {
    puts("Index:");
    unsigned int idx = read_uint();
    if (idx >= N_CHUNKS) {
        puts("aja baja!");
        return;
    }

    read_buf(chunks[idx].buf, chunks[idx].size);
}

void delete_chunk() {
    puts("Index:");
    unsigned int idx = read_uint();
    if (idx >= N_CHUNKS) {
        puts("aja baja!");
        return;
    }
    chunks[idx].buf  = 0;
    chunks[idx].size = 0;
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
                alloc_chunk();
            break;
            case 2:
                read_chunk();
            break;
            case 3:
                write_chunk();
            break;
            case 4:
                delete_chunk();
            break;
            case 5:
                done = 1;
            break;
        }
    }

    return 0;
}
