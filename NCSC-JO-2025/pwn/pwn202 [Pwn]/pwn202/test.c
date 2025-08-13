#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void check(char* password);

void win() {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("[!] Failed to open flag file.");
        exit(1);
    }
    char flag[128];
    fgets(flag, sizeof(flag), f);
    printf("Flag: %s", flag);
    fclose(f);

}

int main(void) {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    printf("Hey please enter the Secret password for lab 202 mr pwner:\n");
    char password[300];

    fgets(password, sizeof(password), stdin);
    password[strcspn(password, "\n")] = 0; 
    
    check(password);
    return 0;
}

void check(char* password) {
    char buffer[10];
    int user_win = 0;
    unsigned char length = strlen(password);

    printf("Length of your input is: %d\n", length);
    
    if (length >= 4 && length <= 8) {
        strcpy(buffer, password);
        if (user_win == 0x49693121) {
            win();
        } else {
            printf("are you sure ? Not the password mr Pwner !\n");
        }
    } else {
        printf("hey ! you must Keep the length between 4 and 8, I can see you are doing a overflow !!\n");
    }
}
