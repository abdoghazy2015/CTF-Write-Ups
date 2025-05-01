#!/bin/sh

echo $FLAG > /flag_$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 20 | head -n 1)
unset FLAG
echo "Challenge started."
su ctf -c "./ynetd -p $PORT ./main"
