### PyGuard

TLDR:
1. Use a characters that have more than 1 byte in it's utf-8 representation (like emojies) to bypass the python guard
2. load the get_line_by_err libc symbol into the debug string (option 1)
3. overwrite only the last byte of the get_line_by_err by \x58 -> __environ libc address (holds a pointer that points to a stack address that points to another stack address that holds the system env)
4. Use the primitive read to get the stack address from the __environ libc address
5. Get a stack address that holds libc address from the leaked stack address and leak it using the primitive read
6. Get the libc address and do ret2libc