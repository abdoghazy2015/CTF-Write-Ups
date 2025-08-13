// journal.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Array to store pointers to our journal entries
void *entries[10];

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_menu() {
    puts("\n==== Secure Journal v1.0 ====");
    puts("1. Create Entry");
    puts("2. View Entry");
    puts("3. Exit");
    printf(">> ");
}

void create_entry() {
    int idx;
    printf("Enter index for new entry (0-9): ");
    scanf("%d", &idx);
    getchar(); // consume newline

    if (idx < 0 || idx >= 10) {
        puts("Invalid index!");
        return;
    }

    if (entries[idx] != NULL) {
        puts("Index already in use.");
        return;
    }

    entries[idx] = malloc(0x40);
    if (!entries[idx]) {
        puts("Allocation failed!");
        exit(1);
    }

    printf("Enter your secret thoughts: ");
    read(0, entries[idx], 0x3f);
    puts("Entry created.");
}

void view_entry() {
    int idx;
    printf("Enter index to view (0-9): ");
    scanf("%d", &idx);
    getchar(); 

    if (idx < 0 || idx >= 10 || entries[idx] == NULL) {
        puts("Invalid or empty index!");
        return;
    }

    puts("--- Entry Content ---");
    // Using puts to print the content. This is important for the leak.
    puts(entries[idx]);
    puts("---------------------");
}
// write what where ? 
// vulnerability
void secret_admin_feature() {
    unsigned long long what, where;

    printf("Admin Override Engaged.\n");
    printf("Enter memory address to write to (in hex): ");
    scanf("%llx", &where);

    printf("Enter value to write (in hex): ");
    scanf("%llx", &what);
    getchar(); 

    printf("Writing 0x%llx to address 0x%llx...\n", what, where);
    *(unsigned long long *)where = what;
    puts("Write complete.");
}


int main() {
    int choice;
    setup();

    puts("Welcome to your personal journal.");

    while(1) {
        print_menu();
        scanf("%d", &choice);
        getchar(); // consume newline

        switch(choice) {
            case 1:
                create_entry();
                break;
            case 2:
                view_entry();
                break;
            case 3:
                puts("Goodbye!");
                exit(0);
                break;
            // The hidden option that triggers the vulnerability
            case 1337:
                secret_admin_feature();
                break;
            default:
                puts("Invalid choice.");
                break;
        }
    }

    return 0;
}
