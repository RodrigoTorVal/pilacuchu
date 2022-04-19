#!/bin/sh
/usr/local/bin/noip2
cd /home/rodrigo/Desktop/servidor/
sh ./start.sh & python3 ./mcChatBotSend.py & python3 ./mcChatBotRec.py & python3 ./mcTimeOut.py
