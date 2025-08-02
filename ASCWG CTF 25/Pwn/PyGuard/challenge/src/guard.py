import os
import pty
import sys
import select

import termios, tty


BINARY = "./app"
MAX_INPUT = 40

def set_raw(fd):
    attr = termios.tcgetattr(fd)
    attr[3] = attr[3] & ~(termios.ECHO | termios.ICANON | termios.ISIG | termios.IEXTEN)
    attr[1] = attr[1] & ~termios.OPOST
    termios.tcsetattr(fd, termios.TCSANOW, attr)


def main():
    # Get input from user
    print(f"Enter your input (max {MAX_INPUT} bytes): ", end='', flush=True)
    user_input = input("")
    if len(user_input) > MAX_INPUT:
        print("[-] Input too long!")
        sys.exit(1)

    # Spawn a pseudo-terminal to simulate interactive shell
    pid, fd = pty.fork()

    if pid == 0:
        # Child process: replace with the target binary
        os.execv(BINARY, [BINARY])
    else:
        set_raw(fd)
        try:
            # Send initial payload
            os.write(fd, user_input.encode() + b'\n')
            while True:
                rlist, _, _ = select.select([sys.stdin, fd], [], [])

                if sys.stdin in rlist:
                    data = sys.stdin.buffer.readline()
                    if not data:
                        break
                    os.write(fd, data)

                if fd in rlist:
                    try:
                        output = os.read(fd, 1024)
                        if not output:
                            print("[+] Process exited.")
                            break
                        sys.stdout.buffer.write(output)
                        sys.stdout.flush()
                    except OSError:
                        break

        except KeyboardInterrupt:
            print("\n[+] Exiting.")
        finally:
            try:
                os.close(fd)
            except Exception:
                pass

if __name__ == "__main__":
    main()
