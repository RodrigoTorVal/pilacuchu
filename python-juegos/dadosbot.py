import requests
import time
import traceback
import random

def sendmsg(text,chat_id,token,mas=""):
	try:
		x=requests.get(r'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s%s'%(token,chat_id,text,mas))
	except Exception:
		print("BOTTEXT ERROR")
		traceback.print_exc()
	return x

def editmsg(chat_id,msg_id,txt,token,mas=""):
	try:
		requests.get(r'https://api.telegram.org/bot%s/editMessageText?chat_id=%s&message_id=%s&text=%s%s'%(token,chat_id,msg_id,txt,mas))
	except Exception:
		print("EDITMSGTXT ERROR")
		traceback.print_exc()

offsetfn="eloffset.dat"

try:
	f=open(offsetfn,"r")
	offset=int(f.readline())
	f.close()
except:
	offset=1
offset_old=offset-1

###################################################################################################
token=""
###################################################################################################

tirar=r'&reply_markup={"inline_keyboard":[[{"text":"TIRAR","callback_data":"tirar"}]]}'
revelar=r'&reply_markup={"inline_keyboard":[[{"text":"REVELAR","callback_data":"revelar"}]]}'
T={}

while True:
	user_id=""
	try:
		url=r'https://api.telegram.org/bot%s/getUpdates?offset=%s&timeout=10'%(token,offset)
		res=requests.get(url).json()
		if "result" in res:
			for item in res["result"]:
				offset=item["update_id"]+1
				if "message" in item and "text" in item["message"]:
					user=" ".join([item["message"]["from"]["first_name"],item["message"]["from"]["last_name"]])
					user_id=str(item["message"]["from"]["id"])
					chat=item["message"]["chat"]["title"]
					chat_id=str(item["message"]["chat"]["id"])
					if item["message"]["text"]=="/dados":
						sendmsg("Agitando cubilete...",chat_id,token,tirar)
				elif "callback_query" in item:
					user=" ".join([item["callback_query"]["from"]["first_name"],item["callback_query"]["from"]["last_name"]])
					user_id=str(item["callback_query"]["from"]["id"])
					chat=item["callback_query"]["message"]["chat"]["title"]
					chat_id=str(item["callback_query"]["message"]["chat"]["id"])
					if item["callback_query"]["data"]=="tirar":
						tirada="%i , %i"%(random.randrange(1,7),random.randrange(1,7))
						T[chat_id]="%s sacó:\n%s"%(user,tirada)
						xx=sendmsg("\n@\n".join([tirada,chat]),user_id,token)
						editmsg(chat_id,item["callback_query"]["message"]["message_id"],"¡Tirada realizada!",token,revelar)
					elif item["callback_query"]["data"]=="revelar":
						if chat_id in T:
							editmsg(chat_id,item["callback_query"]["message"]["message_id"],T[chat_id],token,tirar)
						else:
							editmsg(chat_id,item["callback_query"]["message"]["message_id"],"Agitando cubilete...",token,tirar)
				offset_old=offset
				ff=open(offsetfn,"w")
				ff.write(str(offset))
				ff.close()
	except Exception:
		print("MAIN LOOP ERROR")
		traceback.print_exc()
		time.sleep(1)

