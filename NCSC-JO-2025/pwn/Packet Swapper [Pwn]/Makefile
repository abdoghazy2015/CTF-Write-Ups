# Makefile for the Type Confusion CTF Challenge

CC = gcc
CFLAGS = -fno-stack-protector -no-pie -g
TARGET = test

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c

clean:
	rm -f $(TARGET)
