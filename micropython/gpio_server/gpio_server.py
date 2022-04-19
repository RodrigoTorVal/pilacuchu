from ntptime import settime
import utime
try:
	import usocket as socket
except:
	import socket
from machine import Pin
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
ssid="GALERIA"
password="tirotidritigo"
station=network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected()==False:
	pass
print("Connection successful")
print(station.ifconfig())
settime()
def hora():
	return utime.localtime(utime.mktime(utime.localtime())+2*3600)
led=Pin(4,Pin.OUT)
def web_page(led):
	if led.value()==1:
		gpio_state="ON"
	else:
		gpio_state="OFF"
	html="""<html><head><title>Enchufe WiFi</title><meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}.button2{background-color: #4286f4;}</style></head><body>"""+str(hora())+"""<h1>Enchufe WiFi</h1> <p>Estado: <strong>"""+gpio_state+"""</strong></p><p><a href="/?led=on"><button class="button">ON</button></a><a href="/?led=off"><button class="button button2">OFF</button></a></p><h1>Programar encendido</h1><form action="/">&nbsp &nbsp Inicio: <input type="text" name="Ihrs" size=1>h <input type="text" name="Imns" size=1>m<br>&nbsp Retardo: <input type="text" name="Rhrs" size=1>h <input type="text" name="Rmns" size=1>m<br>Duración: <input type="text" name="Dhrs" size=1>h <input type="text" name="Dmns" size=1>m<br><p><input type="checkbox" name="repe" value="ON">Repetición</p><input type="checkbox" name="L" value="ON">Lunes<br><input type="checkbox" name="M" value="ON">Martes<br><input type="checkbox" name="X" value="ON">Miércoles<br><input type="checkbox" name="J" value="ON">Jueves<br><input type="checkbox" name="V" value="ON">Viernes<br><input type="checkbox" name="S" value="ON">Sábado<br><input type="checkbox" name="D" value="ON">Domingo<br><br><input type="submit" value="Programar"></form></body></html>"""
	return html
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.settimeout(10)
s.bind(("",80))
s.listen(5)
week={"L":0,"M":1,"X":2,"J":3,"V":4,"S":5,"D":6}
repe=False
rep=[]
while True:
	try:
		conn,addr=s.accept()
		print("Got a connection from %s" % str(addr))
		request=conn.recv(1024)
		request=str(request)
		print("Content = %s"%request)
		if request.find("GET")==2:
			RL=request[2:].split("HTTP")[0].split(" ")[1][2:].split("&")
			for n,i in enumerate(RL):
				if i[-1]=="=":
					RL[n]=i+"0"
			print(RL)
			led_on=request.find("/?led=on")
			led_off=request.find("/?led=off")
			if led_on==6:
				print("LED ON")
				led.value(1)
			if led_off==6:
				print("LED OFF")
				led.value(0)
			if "repe=ON" in request:
				repe=True
				rep=[]
				for day in week:
					if day+"=ON" in request:
						rep.append(day)
				print(repe)
			else:
				repe=False
			response=web_page(led)
			conn.sendall(response)
			conn.close()
		else:
			print("ERROR")
			conn.send("ERROR")
			conn.close()
	except:
		print("AGAIN")
