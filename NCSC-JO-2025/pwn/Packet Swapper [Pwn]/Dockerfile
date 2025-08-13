FROM theflash2k/pwn-chal:2504


RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
       libstdc++6 \
       libpthread-stubs0-dev \
       ca-certificates \
       libc6 \
       lib32gcc-s1 \
       libc6:i386 \
       libc6-dev-i386 \
       gcc-multilib \
       procps \
    && rm -rf /var/lib/apt/lists/*


ENV CHAL_NAME=test
ENV PORT=2007
ENV FLAG=NCSC{e2afa4495e8900ad46203c312750034f}
COPY ${CHAL_NAME} .
# COPY flag.txt . 
