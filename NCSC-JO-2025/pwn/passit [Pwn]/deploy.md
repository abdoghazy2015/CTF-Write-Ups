### Idea : 

    Simple ROP challenge to set the first 2 parameters in win function

to build
 
```
docker build -t passit .
```

to run the challange, note do not change the second port

```
docker run -d --rm --name passit -p 8000:8000 passit
```
