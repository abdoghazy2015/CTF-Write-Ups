#!/usr/bin/env python3

from pwn import *

exe = ELF("./gradeViewer_patched")

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
    r.recvuntil("ID: ")
    r.sendline("-62482")
    r.recvuntil("Enter your password [a-z, 0-9]:")
    r.sendline("f1shc0de") # Got it from password_brute scripts
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
