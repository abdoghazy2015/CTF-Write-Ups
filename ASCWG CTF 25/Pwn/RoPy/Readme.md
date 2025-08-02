### RoPy

TLDR:

A.
1. Return to read to write over a writeable area at the binary (/bin/sh)
2. Write the SROP gadgets chain after /bin/sh\0 
3. Do stack pivoting into the writeable area that have your SROP gadgets chain and let the new stack execute them

B.
1. Use syscall write to leak GOT
2. Classic ret2libc
