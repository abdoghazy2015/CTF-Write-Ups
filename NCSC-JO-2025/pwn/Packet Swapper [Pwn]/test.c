// this challnage was suppose to be type confusion exploit 
// but due I wrote it in fast way the exploitation was very is as stack Buffer over flow 
// but I will show the inteded solution as type confusion
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Define packet types
#define TYPE_DATA 0
#define TYPE_CONTROL 1

// Structure for a simple data packet
typedef struct {
    char data[64];
} DataPacket;

typedef struct {
    int auth_level;
    void (*handler)();
} ControlPacket;


void* packet_storage[16];
int packet_types[16];
int packet_count = 0;

void default_handler() {
    puts("Executing default control packet handler...");
}

void win() {
    puts("Congrats! You got a shell!");
    system("/bin/sh");
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void create_packet() {
    if (packet_count >= 16) {
        puts("Packet storage is full.");
        return;
    }

    int type;
    printf("Enter packet type (0=Data, 1=Control): ");
    scanf("%d", &type);

    if (type == TYPE_DATA) {
        DataPacket* packet = (DataPacket*)malloc(sizeof(DataPacket));
        memset(packet->data, 0, sizeof(packet->data));
        puts("Data packet created.");
        packet_storage[packet_count] = packet;
        packet_types[packet_count] = TYPE_DATA;
    } else if (type == TYPE_CONTROL) {
        ControlPacket* packet = (ControlPacket*)malloc(sizeof(ControlPacket));
        packet->auth_level = 0; // Default low-privilege
        packet->handler = default_handler;
        puts("Control packet created.");
        packet_storage[packet_count] = packet;
        packet_types[packet_count] = TYPE_CONTROL;
    } else {
        puts("Invalid packet type.");
        return;
    }
    packet_count++;
}

void edit_data_packet() {
    int index;
    printf("Enter packet index to edit: ");
    scanf("%d", &index);

    if (index < 0 || index >= packet_count) {
        puts("Invalid index.");
        return;
    }
    if (packet_types[index] != TYPE_DATA) {
        puts("Error: Can only edit Data packets.");
        return;
    }

    DataPacket* packet = (DataPacket*)packet_storage[index];
    printf("Enter new data (up to 63 bytes): ");
    // Clear the input buffer before reading new data
    while(getchar() != '\n');
    read(0, packet->data, 63);
    puts("Data updated.");
}

void upgrade_packet() {
    int index;
    printf("Enter packet index to upgrade: ");
    scanf("%d", &index);

    if (index < 0 || index >= packet_count) {
        puts("Invalid index.");
        return;
    }

    if (packet_types[index] == TYPE_DATA) {
        puts("Upgrading Data packet to Control packet...");
		
        packet_types[index] = TYPE_CONTROL;
        puts("Upgrade complete.");
    } else {
        puts("Packet is not a Data packet.");
    }
}

void process_packet() {
    int index;
    printf("Enter packet index to process: ");
    scanf("%d", &index);

    if (index < 0 || index >= packet_count) {
        puts("Invalid index.");
        return;
    }

    if (packet_types[index] != TYPE_CONTROL) {
        puts("Error: Can only process Control packets.");
        return;
    }

    ControlPacket* packet = (ControlPacket*)packet_storage[index];
	
    packet->handler();
}

void menu() {
    puts("\n--- Packet Swapper 9000 ---");
    puts("1. Create Packet");
    puts("2. Edit Data Packet");
    puts("3. Upgrade Data Packet");
    puts("4. Process Control Packet");
    puts("5. Exit");
    printf("> ");
}

int main() {
    setup();

    int choice;
    while (1) {
        menu();
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                create_packet();
                break;
            case 2:
                edit_data_packet();
                break;
            case 3:
                upgrade_packet();
                break;
            case 4:
                process_packet();
                break;
            case 5:
                exit(0);
            default:
                puts("Invalid choice.");
        }
    }
    return 0;
}
