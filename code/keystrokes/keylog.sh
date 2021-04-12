#!/bin/bash

KEYLOG=tripp
trap "echo exiting; exit;" SIGINT SIGTERM

for i in $(seq 255)
do
    echo "starting showkey session"
    sudo stdbuf -o0 showkey | python3 ./keylogger.py ${KEYLOG}.${i}.txt
    echo "logged session to ${KEYLOG}.${i}.txt"
done
