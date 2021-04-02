#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>

#include <sys/ptrace.h>

#define MAX_INPUT 128

extern unsigned char TARGET[];
extern size_t TARGET_LEN;

#define RC4_N 256   // 2^8

void swap(unsigned char *a, unsigned char *b) {
    unsigned char tmp = *a;
    *a = *b;
    *b = tmp;
}

int KSA(const char *key, unsigned char *rc4_state, const size_t keylen) {
    int j = 0;

    for(int i = 0; i < RC4_N; i++)
        rc4_state[i] = i;

    for(int i = 0; i < RC4_N; i++) {
        j = (j + rc4_state[i] + key[i % keylen]) % RC4_N;
        swap(&rc4_state[i], &rc4_state[j]);
    }

    return 0;
}

int PRGA(unsigned char *rc4_state, const unsigned char *plaintext, unsigned char *ciphertext, const size_t len) {

    int i = 0;
    int j = 0;

    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == 0) {
        i = 1;
        j = 1;
    }

    for(size_t n = 0; n < len; n++) {
        i = (i + 1) % RC4_N;
        j = (j + rc4_state[i]) % RC4_N;

        swap(&rc4_state[i], &rc4_state[j]);
        int rnd = rc4_state[(rc4_state[i] + rc4_state[j]) % RC4_N];

        ciphertext[n] = rnd ^ plaintext[n];
    }

    return 0;
}

int RC4(const char *key, const size_t keylen, const unsigned char *plaintext, unsigned char *ciphertext, const size_t len) {

    unsigned char rc4_state[RC4_N];
    KSA(key, rc4_state, keylen);

    PRGA(rc4_state, plaintext, ciphertext, len);

    return 0;
}

int main() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("Fool!\n");
        return 1;
    }

    char input[MAX_INPUT+1];
    const char msg[] = "You fool! No man can kill me!\n";
    printf(msg);
    fgets(input, MAX_INPUT, stdin);

    size_t input_len = strlen(input);
    if(input_len == 0) {
        printf("You need to do *something*\n");
        return 1;
    }

    if(input[input_len-1] == '\n') {
        input[input_len-1] = 0;
    }

    for(size_t idx = 0; idx < input_len; idx++) {
        input[idx] = (input[idx] << 4) | (input[idx] >> 4);
    }

    unsigned char x = 0x13;
    unsigned char y = 0x37;
    for(size_t idx = 0; idx < (input_len+2-1)/2; idx++) {
        input[2*idx] ^= x;
        input[2*idx+1] ^= y;
        y = input[2*idx+1];
        x = input[2*idx];
    }

    RC4(msg, strlen(msg), (unsigned char*)input, (unsigned char*)input, 2*((input_len+2-1)/2));

    if(!memcmp(TARGET, input, TARGET_LEN)) {
        printf("*stab* https://youtu.be/wmUKSZWVQvo?t=20\n");
    } else {
        printf("Die now!\n");
    }
    
    return 0;
}
