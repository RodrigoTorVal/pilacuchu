#-*- coding:utf-8 -*-
#mcChatBot by RodrigoTorVal
#mcChatBot mix your Minecraft server chat and a Telegram group of your choice, together, using a Telegram bot
#this script processes Minecraft chat messages in order to resend them to the group
#in order to get your server verbose into a file, run "java -jar (your_server).jar > server.out"
#you have to define your Telegram group ID as well as your bot token and RCON PARAMETERS
#feel free to report other information from the server by adding more elif's

import requests
from time import sleep

def bottext(text,ID,token):
	#bot texts to ID rutine
	try:
		requests.get("https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s"%(token,ID,text))
	except:
		print("BotRequestError")
	return text

token=
GROUP_ID=

#sleep(10)
print("RecReady!")
f=open("./server.out","r") #this is script is asumed to be at the same location of the server
while True:
	#sleep(0.1)
	try:
		where=f.tell()
		line=f.readline()
		if not line:
			f.seek(where)
		elif "joined the game" in line or "left the game" in line:
			text=line.split("[Server thread/INFO]: ")[1][:-1]
			print(bottext(text,GROUP_ID,token))
		elif "[Server thread/INFO]: <" in line:
			text=line.split("[Server thread/INFO]: ")[1][:-1]
			print(bottext(text,GROUP_ID,token))
		elif "[Server]" in line:
			text="[Server]"+line.split("[Server]")[1][:-1]
			print(bottext(text,GROUP_ID,token))
		elif "[Rcon]" in line and not("[Rcon] §3(Telegram)" in line):
			text="[Rcon]"+line.split("[Rcon]")[1][:-1]
			print(bottext(text,GROUP_ID,token))
	except:	#except Exception as e:
		print("FATAL ERROR")
		sleep(1)
f.close()
