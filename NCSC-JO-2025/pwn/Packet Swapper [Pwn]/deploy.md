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
