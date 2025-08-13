### Idea : 

    Abusing OOB read to leak a libc base from stack and do classic ret2libc attack


docker build -t babypwn . 
docker run -d --rm --name babypwn -p 8000:8000 babypwn
