FROM ubuntu:noble@sha256:c4570d2f4665d5d118ae29fb494dee4f8db8fcfaee0e37a2e19b827f399070d3

# 1. Install minimal Python from Debian repos (more stable)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        socat \
    && rm -rf /var/lib/apt/lists/*

# 2. Create CTF user
RUN useradd -d /home/ctf/ -s /bin/bash ctf

WORKDIR /home/ctf/

# Copy files
COPY ./src/app  .
COPY ./src/flag .
COPY ./src/guard.py .
COPY ynetd .


# Set permissions
RUN chown -R root:root .
RUN chmod 555 app
RUN chmod 555 ynetd
RUN chmod 444 ./flag
USER ctf
EXPOSE 8083
CMD ["./ynetd", "-p", "8083", "python3 guard.py"]