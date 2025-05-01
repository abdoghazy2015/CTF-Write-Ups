### Brief

This is an easy Pwn challenge where the application has some basic features (Register, Login, View Profile and Send Letter)<br>
PIE is enabled but the stack is executable. <br>
There is a format string bug in the view profile function so, the user can leak an address from the stack and calculates the offset between it and the shell code then return to it using the bof bug in the send letter.




### Solution Approaches


1. **Leaking the address from the stack**

    Regsiter a user using %p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p to leak some address from the stack (index 6 must be the $rsp value) which is the stack pointer (top of the stack)


2. **Get the shellcode address offset from the leaked address**

    After doing a breakpoint at send_letter function we can determine the address of our input returning from gets.
    By calculating the offset between our input address (shellcode) and leaked address (leaked address - shellcode address (the top of the stack) = 0x120)

---

### Final Exploit


1. Register and login with : "%6$p"
2. Go to show_profile and get the leaked address then add - 0x120
3. Put the shellcode then padding the rest of buffer by "A" * (264 - len(shellcode) ) to control the RIP
4. Put the address of the shellcode
5. Get a shell

[Here is the exploit script](./solve.py)

This script automates the steps described above to exploit the vulnerability and gain a shell.

![alt text](image-1.png)