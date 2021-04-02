#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT 128

int main() {
    char input[MAX_INPUT];
    printf("Speak friend and enter!\n");
    fgets(input, MAX_INPUT, stdin);

    size_t input_len = strlen(input);
    if(input_len > 0 && input[input_len-1] == '\n') {
        input[input_len-1] = 0;
    }

    if(!strcmp("SSM{Annon_edhellen_edro_hi_ammen_m3llon}", input)) {
        printf("What's the Elvish word for friend? https://youtu.be/DgHCM68KkPY?t=238\n");
    } else {
        printf("Nothing happens.\n");
    }

    return 0;
}
