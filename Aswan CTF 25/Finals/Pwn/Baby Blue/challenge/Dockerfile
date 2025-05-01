FROM kalilinux/kali-rolling

# Create CTF user
RUN useradd -d /home/ctf/ -s /bin/bash ctf
RUN apt-get update

WORKDIR /home/ctf/

# Copy files
COPY ./src/baby_blue  .
COPY ./src/flag .
COPY ./src/libc.so.6  .
COPY ./src/ld-linux-x86-64.so.2  .
COPY ynetd .

# Set permissions
RUN chown -R root:root .
RUN chmod 555 baby_blue
RUN chmod 555 libc.so.6
RUN chmod 555 ld-linux-x86-64.so.2
RUN chmod 555 ynetd
RUN chmod 444 ./flag

USER ctf
EXPOSE 8083
CMD ["./ynetd", "-p", "8083", "./baby_blue"]
