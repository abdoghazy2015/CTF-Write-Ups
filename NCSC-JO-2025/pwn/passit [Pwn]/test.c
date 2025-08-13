#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__asm__(
    ".global pop_rdi_ret            \n"
    "pop_rdi_ret:                   \n"
    "    pop %rdi                   \n"
    "    ret                        \n"
    ".global pop_rbp_pop_rsi_ret    \n"
    "pop_rbp_pop_rsi_ret:           \n"
    "    pop %rbp                   \n"
    "    pop %rsi                   \n"
    "    ret                        \n"
);

__attribute__((constructor))
void __constructor__(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(long first, long second) {
    if (first == 0x00435343434e0000 && second == 0x005a44494b530000){
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("[!] Failed to open flag file.");
        exit(1);
    }
    char flag[128];
    fgets(flag, sizeof(flag), f);
    printf("Flag: %s", flag);
    fclose(f);
   }else{
	puts("[!] opppa I have miss it !");
   }
}

void vuln() {
    char buf[64];
    puts("pass the ball to me, to give you the flag !");
    puts("pass it now ! :");
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
