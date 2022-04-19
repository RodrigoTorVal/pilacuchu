#-*- coding:utf-8 -*-
#mcChatBot by RodrigoTorVal
#mcChatBot mix your Minecraft server chat and a Telegram group of your choice, together, using a Telegram bot
#this script processes group messages in order to resend them to the minecraft chat
#you have to define your Telegram group ID as well as your bot token and RCON PARAMETERS
#you also have to define the Telegram ID of who will able to use the rcon console
#feel free to add any other functios on GROUP COMMANDS SECTION conditional

import mcrcon
import requests
from time import sleep

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
		rcon.connect("localhost", 25575, "passss")	#RCON PARAMETERS
		out = rcon.command(comando)
		rcon.disconnect()
	except:
		out="ServerConnectionError"
	print(out)
	return out

def control(comando,ID,token):
	#rcon console bot implementation
	Cout=command(comando)
	bottext(Cout,ID,token)
	return Cout
	
try:	#try to load bot collection offset
	ff=open("offset.dat","r")
	offset=int(ff.readline())
	ff.close()
except:
	offset=1
offset_old=offset-1

token=
GROUP_ID=
CONTROL_ID=

sleep(30)
print("SendReady!")
while True:
	sleep(0.1)
	try:
		#collect bot msg
		url="https://api.telegram.org/bot%s/getUpdates?offset=%s&timeout=30"%(token,offset)
		res=requests.get(url).json()
		for item in res["result"]:
			offset=item["update_id"]+1
			print(offset)
			msg=item["message"]
			if "text" in msg:	#only text filter
				chat_id=msg["chat"]["id"]
				text = msg["text"]
				try:	#check for Telegram user alias
					who=msg["from"]["username"]
				except:	#tell your friends to choose an alias
					who="UnknownUser"
				if offset>offset_old:
					#######remote console begins#######
					if chat_id==CONTROL_ID and text[0]=="/":
						control(text,CONTROL_ID,token)
						print("Controlled!")
					#######remote console ends#######
					elif chat_id==GROUP_ID:
						if text[0]=="/" and text!="/xxxxx":		#GROUP COMMANDS SECTION
							if text=="/list" or text=="/list@MineServerChatBot":	#show who is connected to group
								bottext(command("list"),chat_id,token)
						else:
							command("say §3(Telegram)"+" §6"+who+"§f: "+msg["text"])	#resend text msg from group to server
						print("ChatId: "+str(chat_id))	#sender ID
						print(text)						#text message from ID
				offset_old=offset
				ff=open("offset.dat","w")	#save offset
				ff.write(str(offset))
				ff.close()
	except:	#except Exception as e:
		print("FATAL ERROR")
		sleep(1)
