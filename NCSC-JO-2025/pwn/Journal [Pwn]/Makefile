IMG=pwn-chal:2504-sample

all: chal container
chal:
	gcc -o test test.c -w
container:
	docker build -t $(IMG) .
run:
	docker run -it --name pwnchal --cap-add NET_ADMIN --rm -p31337:8000 $(IMG)
