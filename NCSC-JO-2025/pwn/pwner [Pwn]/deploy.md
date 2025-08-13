# enable ASLR on the Host


to build
 
```
docker build -t pwner .
```

to run the challange, note do not change the second port

```
docker run -d --rm --name pwner -p 8000:8000 pwner
```
