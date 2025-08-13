// A pwn challenge to demonstrate OOB Read + ROP 
//
// Compile with PIE enabled:
// gcc chall.c -o chall -fno-stack-protector -pie

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vulnerable_function() {
    // We use a long array to make stack indexing cleaner (8 bytes per element)
    long data[4];
    char buffer[32];
    int index;

    printf("I have a secret on my stack. Try to find it.\n");
    printf("Index > ");
    scanf("%d", &index);

    // OOB Read vulnerability: No bounds check on the index
    printf("Leaking for you: 0x%lx\n", data[index]);

    printf("Now, give me your data payload.\n> ");
    // Clear the trailing newline from scanf so it doesn't interfere with read()
    getchar();

    // Buffer overflow vulnerability using read()
    // The program attempts to read up to 128 bytes into a 32-byte buffer.
    ssize_t bytes_read = read(STDIN_FILENO, buffer, 128);

    printf("Received %ld bytes. Bye!\n", bytes_read);
}

int main() {
    setup();
    puts("Welcome to the Pwn360 challenge!");
    vulnerable_function();
    return 0;
}
