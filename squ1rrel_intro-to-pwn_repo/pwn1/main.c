#include <stdio.h> 
#include <stdlib.h> 


int main(){
    char buf[0x100];
    int overwrite_me;
    overwrite_me = 1234;
    puts("Welcome to PWN 101, smash my variable please.\n"); 
    gets(buf);
    if (overwrite_me == 0x1337){ 
        system("/bin/sh");
    } 
    return 0; 
}