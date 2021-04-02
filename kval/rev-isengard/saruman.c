#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>

#define MAX_INPUT 128

extern unsigned char TARGET[];
extern size_t TARGET_LEN;

int main() {
    char input[MAX_INPUT+1];
    printf("What do you want, Gandalf Greyhame?\n");
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
        input[idx] += 2*(idx+1);
    }

    uint16_t *input2 = (uint16_t*)input;
    for(size_t idx = 0; idx < (input_len+2-1)/2; idx++) {
        input2[idx] ^= 0x1337;
    }


    if(!memcmp(TARGET, input, TARGET_LEN)) {
        printf("*gasp* https://youtu.be/djmahoN32A8?t=283\n");
    } else {
        printf("Save your pity and your mercy! I have no use for it!\n");
    }
    
    return 0;
}
