#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_TEMPLATES 6
#define FLAG_LEN 64

char *premium_template = 
"     __\n"
"  .'`  `'.\n"
" /        \\ _\n"
";      __.'` `'.\n"
"|   .'`  `'.    \\\n"
";  / HAPPY  \\    ;\n"
" \\;   %2$dth    ;   |\n"
"  | BIRTHDAY |   ;   _\n"
"  ; %1$8s ;-./-_-` '-.\n"
"  /\\        /_(;'/ `\\()  '.\n"
" ;  '.__  .'\\|| '    |     '.\n"
" |      ),\\| \\\\      \\()    (\\\n"
" ;        \\ \\|/   __/    ()   \\  __\n"
"  \\        \\||\\.~'_ `'.;-.___.~'` _'~.\n"
"   '.__  _/|/|/{ (_`.'         '.`_) }\n"
"       `)/`\\\\\\\\ \\ .'  _ 0_._0 _  '. /     .,_\n"
"             \\|| } -.'   (_)   '.- {    _{   `\\\n"
"              \\|{_ / '.___|___.' \\  }  //`._   |\n"
"            /`    \\     |   |     }  }:'-.  ```'\"--..==,\n"
"           {      ,}    \\-\"-/   .'  } {,`-'.       //>`\\>\n"
"          {`   _./|\\._.  '-'  ._ .~` /`    ;'.    //>  |>\n"
"          {     {///(  `-.-.-`  ) _.'     /   '. ||>   />\n"
"           \\     \\|\\);--`( )`--`(`       }      `\\\\>_.'>\n"
"            ;  _/`/(__.'/`-'.,__/`,    .`         `\"\"\"`\n"
"           .-'`     ;-.(     \\_(;  \\ .'     .--,\n"
"          (`-._   ./   `       '.   `-._..~` /o\\\\\n"
"           `'-;/``.              `;-\"`:     |oo||\n"
"      .--._ _.' .  \\      o       ;  .      |  /|\n"
"     /.-.  `     .  '._        _.'  '       \\_//\n"
"     ||oo\\        `.   `'-----`  _.~`--..__,..'\n"
"     |\\o  |       .~`'--......--'\n"
"      \\'._/   _.~`\n"
"       `.__.-'\n"
" Here is a special present for your birthday\n"
" %3$s \n";

struct
{
    long age;
    char *name;
    long template;
    char *templates[NUM_TEMPLATES];
} globals = {
    .name = NULL,
    .age = 0,
    .template = -1,
    .templates = {
// Template 1
"       iiiiiiiiii\n"
"      |:H:a:p:p:y:|\n"
"    __|___________|__\n"
"   |^^^^^^^^^^^^^^^^^|\n"
"   |:B:i:r:t:h:d:a:y:|\n"
"   | %15s |\n"
"   ~~~~~~~~~~~~~~~~~~~\n"
"   on your %dth birthday!\n",
// Template 2
"       iiiiiiiiiiiiiiiiiii\n"
"     |||||||H|A|P|P|Y|||||||\n"
"   __|_____________________|__\n"
"  |\\/\\/\\/\\/\\/\\/\\/\\/\\\\/\\/\\/\\/\\/|\n"
"  |||||||B|I|R|T|H|D|A|Y|||||||\n"
"  |,,,,,,,,,,,,,,,,,,,,,,,,,,,|\n"
"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
"   to %s\n"
"   on your %dth birthday!\n",
// Template 3
"                          __\n"
"                        ,"  ".\n"
"     _      .---.    _ /#     \\\n"
"   ,' `.  ,'     `.." ".      ,--.\n"
"   |#   `/ #      (#    )    /    )\n"
"    `.   |         )   (`.__/    /\n"
"      `. \\        (     )/'/    /\n"
"        `.\\       /)   (( /    /\n"
"           `.   .'(     )y    /\n"
"             >_<\\  `._.'(    /\n"
"             /   ) /'-`.->,-'\n"
"            (   ( (   (\n"
"             )     )   ) \n"
"                  (\n"
"   to %s\n"
"   on your %dth birthday!\n",
//Template 4
"              (        (\n"
"             ( )      ( )          (\n"
"      (       Y        Y          ( )\n"
"     ( )     |\"|      |\"|          Y\n"
"      Y      | |      | |         |\"|\n"
"     |\"|     | |.-----| |---.___  | |\n"
"     | |  .--| |,~~~~~| |~~~,,,,'-| |\n"
"     | |-,,~~'-'___   '-'       ~~| |._\n"
"    .| |~       // ___            '-',,'.\n"
"   /,'-'     <_// // _  __             ~,\n"
"  / ;     ,-,     \\\\_> <<_' ____________;_)\n"
"  | ;    {(_)} _,      ._>>`'-._          |\n"
"  | ;     '-'\\_\\/>              '-._      |\n"
"  |\\ ~,,,      _\\__            ,,,,,'-.   |\n"
"  | '-._ ~~,,,            ,,,~~ __.-'~ |  |\n"
"  |     '-.__ ~~~~~~~~~~~~ __.-'       |__|\n"
"  |\\         `'----------'`           _|\n"
"  | '=._      HAPPY BIRTHDAY     __.=' |\n"
"  :     '=.__               __.='      |\n"
"   \\         `'==========='`          .'\n"
"    '-._     %16s    __.-'\n"
"        '-.__               __.-'\n"
"             `'-----------'`\n"
"   on your %dth birthday!\n",
//Template 5
"                 ,\n"
"                (_)\n"
"                |-|\n"
"                | |\n"
"                | |\n"
"               .| |.\n"
"              |'---'|\n"
"              |~  ~~|\n"
"          .-@'|  ~  |'@-.\n"
"         (@    '---'    @)\n"
"         |'-@..__@__..@-'|\n"
"      () |~  ~ ~ ~     ~ | ()\n"
"     .||'| ~() ~   ~ ()~ |'||.\n"
"    ( || @'-||.__~__.||-'@ || )\n"
"    |'-.._  ||   @   ||  _..-'|\n"
"    |~ ~  '''---------'''  ~  |\n"
"    |  ~  ~  H A P P Y ~  ~  ~|\n"
"    | ~   B I R T H D A Y ~ ~ |\n"
"     '-.._%15s_..-'\n"
"          '''---------'''\n"
"   on your %dth birthday!\n",
//Template 6
"   ,-.\n"
"   | |\n"
"   | \"--.  ,--.-.,-.--. ,-.--. ,-. ,-.\n"
"   | ,-. \\/ ,-. || ,-. \\| ,-. \\| | | |\n"
"   | | | |\\ `-' || `-' /| `-' /| `-' |\n"
"   `-' `-' `--'-'| .--' | .--'  `--. |\n"
"                 | |    | |        | |\n"
"                 `-'    `-'        `-'\n"
",-.     _       ,-.  ,-.        ,-.\n"
"| |    (_)      | |_ | |        | |\n"
"| \"--. ,-.,-.--.|  _)| \"--.  ,--\" | ,--.-.,-. ,-.\n"
"| ,-. \\| || ,-./| |  | ,-. \\/ ,-. |/ ,-. || | | |\n"
"| `-' /| || |   | |  | | | |\\ `-' |\\ `-' || `-' |\n"
"\"-'--' `-'`-'   `-'  `-' `-' `--'-' `--'-' `--. |\n"
"                                              | | \n"
"                                              `-'\n"
"   to %s\n"
"   on your %dth birthday!\n",
    }
};

long get_int(void) {
    char int_str[16];
    fgets(int_str, 16, stdin);
    return strtol(int_str, NULL, 10);
}

void set_recipient(void) {
    if(globals.name == NULL) {
        globals.name = malloc(64);
    }
    printf("Who is the card for? ");
    fgets(globals.name, 64, stdin);
    size_t name_len = strlen(globals.name);
    if(name_len > 0 && globals.name[name_len-1] == '\n') {
        globals.name[name_len-1] = '\0';
    }

    printf("How old are they turning? ");
    globals.age = get_int();
    if(globals.age == 0) {
        puts("Please input a valid age");
    }
}

void choose_template(void) {
    puts("The following birthday card templates are available:");
    for (size_t i = 0; i < NUM_TEMPLATES; i++) {
        printf("Template %lu:\n", i+1);
        printf(globals.templates[i], "[Name Here]", 18);
        printf("\n");
    }
    
    puts("Please choose a template");
    int template_choice = get_int();
    if(template_choice == 0) {
        puts("Invalid template choice");
        return;
    }

#ifndef DEBUG
    if(template_choice == 1337) {
        puts("Please contact sales to upgrade to the premium version of the birthday card generator.");
        return;
    }
#endif
    if(template_choice == 1337) {
        globals.template = 1337;
    } else {
        globals.template = abs(template_choice-1) % NUM_TEMPLATES;
    }

    puts("Template set");
}

void premium_card(void) {
    FILE *flag_file = fopen("flag.txt", "r");
    if(flag_file == NULL) {
        printf("System error: Please contact an administrator\n");
        return;
    }
    char flag[FLAG_LEN];
    fgets(flag, FLAG_LEN, flag_file);
    fclose(flag_file);
    puts("Thanks for purchasing the premium version of our birthday card generator");
    puts("Here is your premium birthday card, enjoy!");
    printf(premium_template, globals.name, globals.age, flag);
}

void standard_card(void) {
    puts("Here is your birthday card, enjoy!");
#ifdef DEBUG
    printf("Template index: %d, %p\n", globals.template, globals.templates[globals.template]);
#endif
    printf(globals.templates[globals.template], globals.name, globals.age);
    printf("\n");
}

void generate_card(void) {
    if(globals.name == NULL || globals.age == 0) {
        puts("Please set the recipient before generating a card");
        return;
    }
    if(globals.template == -1) {
        puts("Please choose a greetings card template before generating a card");
        return;
    }
    if(globals.template == 1337) {
        premium_card();
    } else {
        standard_card();
    }
}

void welcome(void)
{
    puts("Welcome to the birthday card generator");
    puts("");
}

int menu(void)
{
    puts("Menu:");
    puts("1. Set recipient");
    puts("2. Choose template");
    puts("3. Generate card");
    puts("4. Exit");

    return get_int();
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    welcome();
    unsigned char running = 1;
    while (running)
    {
        int choice = menu();

        switch (choice)
        {
        case 1:
            set_recipient();
            break;
        case 2:
            choose_template();
            break;
        case 3:
            generate_card();
            break;
        case 4:
            puts("Goodbye!");
            running = 0;
            break;
        default:
            puts("Invalid menu choice");
            break;
        }
    }

    return 0;
}
