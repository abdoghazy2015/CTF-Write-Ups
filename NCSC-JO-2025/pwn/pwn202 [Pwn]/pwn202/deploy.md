### Idea : 

    Abusing integar overflow to bypass a length check and use BOF in strcpy to control some variable


# ASLR must be enabled 


to build
 
```
docker build -t pwn202 .
```

to run the challange, note do not change the second port

```
docker run -d --rm --name pwn202 -p 8000:8000 pwn202
```
