#!/bin/bash
#Send request to google voice recognition. Should be replaced with call to sphinx engine eventually
AUDIODEV=hw:1,0 rec -c 1 -r 16000 /tmp/voice.wav silence 1 0.3 3% 1 0.3 3% > /dev/null
flac -f -s /tmp/voice.wav -o /tmp/voice.flac 2>&1 >/dev/null
curl -X POST --data-binary @/tmp/voice.flac \
 --user-agent 'Mozilla/5.0' \
 --header 'Content-Type: audio/x-flac; rate=16000;' \
 'https://www.google.com/speech-api/v2/recognize?output=json&lang=ru-RU&key=AIzaSyAqk7vE0vQDR3JItUPgFp6bcPqgJz8h8tI'
