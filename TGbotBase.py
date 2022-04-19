import requests
from time import sleep

def bottext(text,ID,token,parse_mode=""):
	try:
		requests.get(r'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=%s'%(token,ID,text,parse_mode))
	except Exception as ex:
		print("bottextERROR",ex,sep="\n")

token=""
offsetfn="TUOoffset.dat"

try:
	ff=open(offsetfn,"r")
	offset=int(ff.readline())
	ff.close()
except:
	offset=1
offset_old=offset-1

while True:
	sleep(0.5)
	try:
		url=r'https://api.telegram.org/bot%s/getUpdates?offset=%s&timeout=30'%(token,offset)
		res=requests.get(url).json()
		for item in res["result"]:
			offset=item["update_id"]+1
			print("Offset:",offset)
			msg=item["message"]
			if "text" in msg:
				chat_id=msg["chat"]["id"]
				text=msg["text"]
				try:
					who=msg["from"]["username"]
				except:
					who="UnknownUser"
				if offset>offset_old:
					if text=='/help' or text=='/start':
						bottext(r'',chat_id,token)
					print("ChatId:",str(chat_id),"\nUser:",who,"\nText:",text)
				offset_old=offset
				ff=open(offsetfn,"w")
				ff.write(str(offset))
				ff.close()
	except Exception as ex:
		print("FATAL ERROR",ex,sep="\n")
		sleep(1)

