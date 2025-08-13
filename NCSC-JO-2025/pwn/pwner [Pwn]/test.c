#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <setjmp.h>
#include <ucontext.h>

jmp_buf jump_buffer;

// Prototype so the handler can take its address
void print_flag(void);

// SIGSEGV handler that prints the faulting EIP and the address of print_flag, then longjmps back
void sigsegv_handler(int signum, siginfo_t *info, void *ucontext) {
    ucontext_t *ctx = (ucontext_t *)ucontext;
    // On 32 bit x86, EIP is in gregs[14]
    unsigned long eip = ctx->uc_mcontext.gregs[14];
    // Get the address of print_flag
    unsigned long flag_addr = (unsigned long)&print_flag;
    //printf("Segmentation fault caught at EIP = 0x%08lx\n", eip);
    //printf("Address of print_flag = 0x%08lx\n", flag_addr);
    siglongjmp(jump_buffer, 1);
}

void print_flag(void) {
    char flag[64];
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        printf("Could not find flag.txt\n");
        exit(1);
    }
    fgets(flag, sizeof(flag), f);
    printf("%s", flag);
    fclose(f);
}

void vulnerable() {
    char buffer[40];
    printf("ASLR is on, good luck!\n");
    printf("> ");
    fflush(stdout);
    read(0, buffer, 100);
}

int main() {
    // Disable buffering on stdout and stdin
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);

    // Install SA_SIGINFO handler so we can inspect ucontext
    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_sigaction = sigsegv_handler;
    sa.sa_flags     = SA_SIGINFO;
    if (sigaction(SIGSEGV, &sa, NULL) == -1) {
        perror("sigaction");
        exit(1);
    }

    // Loop, jumping back here after each SIGSEGV
    while (1) {
        if (sigsetjmp(jump_buffer, 1) == 0) {
            // First time or after a successful longjmp
            vulnerable();
        } else {
            // Returned here from siglongjmp after a crash
	    printf("Recovred ... \n");
        }
    }

    return 0;
}
