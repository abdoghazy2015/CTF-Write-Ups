### Idea : 

    Bruteforcing 1 nibble in the return address (main) to call win function

docker build -t babypwn . 
docker run -d --rm --name babypwn -p 8000:8000 babypwn
