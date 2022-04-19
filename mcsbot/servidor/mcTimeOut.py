#-*- coding:utf-8 -*-
#mcTimeOut for Linux by RodrigoTorVal
#mcTimeOut shutdowns your server and computer if no one is playing after a defined time
#mcTimeOut checks for people playing every minute
#NOTE:	you should have an automated way of starting your server.
#		I have another TG bot on a esp8266 wich starts my computer

import mcrcon
from time import sleep
import os
import requests

def bottext(text,ID,token):
	#bot texts to ID rutine
	try:
		requests.get("https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s"%(token,ID,text))
	except:
		print("BotRequestError")

def command(comando):
	#rcon command rutine
	try:
		rcon = mcrcon.MCRcon()
		rcon.connect("localhost", 25575, "passs")	#RCON PARAMETERS
		out = rcon.command(comando)
		rcon.disconnect()
	except:
		out="ServerConnectionError"
	print(out)
	return out

stop=False
time=0
tout=20 #minutes
token=
GROUP_ID=

sleep(30)
bottext("Server ON",GROUP_ID,token)
sleep(30)
print("TimeOutReady!")
while True:
	sleep(60) #60
	try:
		players = int(command("list").split("/")[0].split(" ")[-1])
		print("Players:",players)
	except:
		players=0
		print("listERROR")
	if players==0:
		time+=1
		if time>=tout:
			stop=True
	else:
		stop=False
		time=0
	if stop:
		try:
			rcon = mcrcon.MCRcon()
			rcon.connect("localhost", 25575, "passsssss")
			print(rcon.command("stop"))
			rcon.disconnect()
			bottext("Server OFF",GROUP_ID,token)
			sleep(10)
			print("ShutingDown...")
			os.system("sh /home/asus/sdown.sh")
			print("ShutdownOK")
			break
		except:	#except Exception as e:
			print("ERROR@STOP")
