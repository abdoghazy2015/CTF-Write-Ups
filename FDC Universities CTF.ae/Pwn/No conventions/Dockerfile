FROM ubuntu@sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f AS app

WORKDIR /app
RUN useradd -m ctf
COPY main .
COPY ynetd .
COPY hook.sh .
RUN chmod +x main hook.sh ynetd
CMD /app/hook.sh
