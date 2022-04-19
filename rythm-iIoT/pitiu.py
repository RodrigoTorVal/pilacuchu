from time import ticks_ms,sleep_ms
from machine import Pin

def blink(pin,time1,time2=0):
	pin.off()
	sleep_ms(time1)
	pin.on()
	sleep_ms(time2)
	
def actuar(pin,time1,time2):
	pin.on()
	sleep_ms(time1)
	pin.off()
	sleep_ms(time2)

def analisis(T,ro=4,N=2):
	TT=[T[i+1]-T[i] for i in range(len(T)-1)]
	LL=[[j/i for j in TT] for i in TT]
	L=sorted(LL)
	for k in range(1,len(L)):
		dd=len(L[k])
		m=0
		for kk in range(dd):
			m+=L[k][kk]/L[k-1][kk]/dd
		mm=round(ro*m)/ro
		L[k]=[q/mm for q in L[k]]
	return [N*round(ro*sum([i[j] for i in L])/len(L))/ro for j in range(len(L[0]))]

def rutina(clave=[2,1,1,2,2],pin=5,rele=4,limin=60,limax=1000):	#(limin=60) ritmos muy rapidos
	PIN=Pin(pin,Pin.IN)
	RELE=Pin(rele,Pin.OUT)
	LED=Pin(16,Pin.OUT)
	T=[]
	estado=[PIN.value(),ticks_ms()]
	estadoanterior=estado[:]
	pi=estado[1]
	pia=estadoanterior[1]
	while True:
		################################################################
		estadoanterior=estado[:]
		estado=[PIN.value(),ticks_ms()]
		if estado[0]==1 and estadoanterior[0]==0:
			pi=estado[1]
			if pi-pia<=limax:
				if pi-pia>=limin:
					T.append(pi)
					print(pi-pia)#blink(LED,10)
			else:
				T=[pi,]
				print(pi-pia)#blink(LED,10)
			pia=estadoanterior[1]
			if len(T)==len(clave):
				A=analisis(T,max(clave)/min(clave),max(clave))
				if A==clave[:-1]:
					sleep_ms(200)
					actuar(RELE,50,200)
					actuar(RELE,50,0)
		################################################################
