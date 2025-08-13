#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor))
void __constructor__(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

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

void vuln() {
    char buf[64];
    puts("Welcome to babypwn challenge!");
    puts("Enter your input:");
    /* unsafe read allows overflow */
    fgets(buf, 200, stdin);
    printf("You said: %s", buf);
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    vuln();
    return 0;
}
