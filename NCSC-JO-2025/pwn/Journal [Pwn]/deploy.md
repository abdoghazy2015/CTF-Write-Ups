### Idea : 

    1. Use WWW to write over entries global array in DATA section (that you can read content by index entries[i]) with a GOT entry
    2. Read this entry and get a libc leak
    3. Create a second entry with "/bin/sh"
    4. Use WWW to write over puts@GOT with system
    5. Read entries[1] to trigger system("/bin/sh")



# disable ASLR on the Host not in the docker container using 


```
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
```
to build
 
```
docker build -t babypwn .
```

to run the challange, note do not change the second port

```
docker run -d --rm --name babypwn -p 8000:8000 babypwn
```
