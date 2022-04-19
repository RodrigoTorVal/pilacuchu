import requests
from time import sleep
import feedparser

def rssget(url):
	feed=feedparser.parse(url)
	entries=feed.entries
	return entries

def bottext(text,ID,token,parse_mode=""):
	try:
		requests.get(r'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=%s'%(token,ID,text,parse_mode))
	except Exception as ex:
		print("bottextERROR",ex,sep="\n")

token="878359764:AAF9AwHd0MRUlyN-Ar3ZyH4e9ZjQcCu8M9Q"

RSS={'Actos':r'http://www.uniovi.es/comunicacion/duo/actos/-/asset_publisher/L2iEKaAZuBNz/rss',
'Anuncios':r'http://www.uniovi.es/comunicacion/duo/anuncios/-/asset_publisher/k22otAqlur25/rss',
'Becas':r'http://www.uniovi.es/comunicacion/duo/becas/-/asset_publisher/ZICH7zdCzufQ/rss',
'Boletines Oficiales':r'http://www.uniovi.es/comunicacion/duo/boletinesoficiales/-/asset_publisher/7iuBUjFjsoD2/rss',
'Convocatorias':r'http://www.uniovi.es/comunicacion/duo/convocatorias/-/asset_publisher/cxX13ntusT2E/rss',
'Otros':r'http://www.uniovi.es/comunicacion/duo/otros/-/asset_publisher/tJrNest4WQMj/rss'}

try:
	ff=open("offset.dat","r")
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
					if text[:7]=="/duoget":
						nf=True
						for j in RSS:
							M=''
							#bottext(j,chat_id,token)
							entries=rssget(RSS[j])
							for i in entries:
								if i and text[7:]=='':
									M+='\n\n'+r'<a href="%s">%s</a>'%(i['link'],i['title'])
									#bottext(i['title']+"\n"+r'<a href="%s">ENLACE</a>'%i['link'],chat_id,token,"HTML")
								elif i and text[6:][1:2]==' ':
									args=text[8:].lower().split(' ')
									if 'boletines' in args and 'oficiales' in args:
										args.remove('boletines')
										args.remove('oficiales')
										args.append('boletines oficiales')
									if sum([k in i['title'].lower() for k in args])>0 or j.lower() in args:
										nf=False
										M+='\n\n'+r'<a href="%s">%s</a>'%(i['link'],i['title'])
										#bottext(i['title']+"\n"+r'<a href="%s">ENLACE</a>'%i['link'],chat_id,token,"HTML")
							if M:
								M=j.upper()+M
							bottext(M,chat_id,token,"HTML")
						if nf and text[6:][1:2]==' ':
							bottext(r'No se han encontrado resultados con "%s".'%text[8:].replace(' ','", "'),chat_id,token)
						
					if text=='/help' or text=='/start':
						bottext(r'''Si utiliza /duoget a secas, recibirá el dUO de hoy al completo.

Si desea realizar una búsqueda por palabras y categorías añádalas al final y separelas por espacios.

Por ejemplo, si envía:
    /duoget becas erasmus definitiva
recibirá la categoría "Becas" al completo y todas las publicaciones que contengan las palabras "becas", "erasmus" y "definitiva".

Las categorías disponibles son:
    Actos
    Anuncios
    Becas
    Boletines Oficiales
    Convocatorias
    Otros
''',chat_id,token)
					print("ChatId:",str(chat_id),"\nUser:",who,"\nText:",text)
				offset_old=offset
				ff=open("offset.dat","w")
				ff.write(str(offset))
				ff.close()
	except Exception as ex:
		print("FATAL ERROR",ex,sep="\n")
		sleep(1)


"""
import feedparser
feed=feedparser.parse("http://www.uniovi.es/comunicacion/duo/boletinesoficiales/-/asset_publisher/7iuBUjFjsoD2/rss")
entries=feed.entries
N=len(entries)
for i in range(N):
	print(entries[i]['title'],entries[i]['link'],sep="\n\t")
"""
