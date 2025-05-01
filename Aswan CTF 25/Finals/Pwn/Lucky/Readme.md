### Brief

This challenge involves exploiting a simple binary to gain shell access. <br>The application generates a "lucky number" using `rand() % 1000`, seeded with `srand(time(0))`. <br>If the user guesses the number correctly, the program calls a function named `gift()`. This function uses the vulnerable `gets()` function to take user input, leading to a buffer overflow (BOF).<br>

Key details:
- **PIE** is disabled.
- The stack is executable.
- No memory leak is provided for user input.

This setup makes it a classic **ret2shellcode** challenge.

---

### Solution Approaches

#### 1. **Retrieve the lucky number**

To predict the lucky number:
- Use `ctypes.CDLL('./libc.so.6')` to load the same libc version as the challenge binary.
- Obtain the current timestamp and use it as the seed for `rand()`.
- Calculate `rand() % 1000` to determine the lucky number.
- Send the lucky number to the application to proceed to the `gift()` function.

#### 2. **Find a gadget to execute the shellcode**

Inside the `gift()` function:
- After setting a breakpoint, observe that the `gets()` function stores the pointer to the user input in the `RAX` register.
- Use a tool like `ropper` to locate a `jmp rax` gadget in the binary. This gadget will allow you to jump directly to your shellcode.

---

### Final Exploit Steps

1. Load the same libc version as the challenge binary.
2. Use the current timestamp to seed `rand()` and calculate the lucky number.
3. Send the lucky number to the application.
4. Craft your payload:
    - Place your shellcode.
    - Pad the buffer with `"A"` characters to fill up to 72 bytes (or the required offset).
    - Append the address of the `jmp rax` gadget.
5. Execute the payload to gain a shell.

[Here is the exploit script](./solve.py)

This script automates the above steps to exploit the vulnerability and achieve shell access.