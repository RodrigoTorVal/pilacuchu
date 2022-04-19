from time import ticks_ms,sleep_ms
from machine import Pin

def analisis(T,ro=4,N=2):
	#ro=4	#parametro de redondeo ; Rx=round(ro*x)/ro ; p.e.: si (ro=4) Rx tiene precision 0.25==(1/ro)
	#la resolucion sera de "1/ro" (normalizando a la figura mas larga)
	#p.e.: si (ro=8) solo se detectaran figuras de redondas a corcheas
	#para detectar hasta semicorcheas "ro" debe ser (ro=16) // 16 semicorcheas hacen cuatro negras o una redonda
	#aparentemente a mayor "ro" mas precisos deben ser los golpes
	#EL COMPORTAMIENTO EN FUNCION DE "ro" DEBE SER ESTUDIADO
	T=T[:-1]	#obvia el ultimo elemento, es irrelevante
	#print(T)
	TT=[T[i+1]-T[i] for i in range(len(T)-1)]	#lista de intervalos entre golpes
	#print(TT)
	#print("")
	LL=[[j/i for j in TT] for i in TT]	#listas de ratios entre intervalos, referrenciados a cada golpe (1 lista por golpe)
				#L=[sorted(LL)[i] for i in range(len(LL)-1,0,-1)]	#ordena LL de mayor a menor
	L=sorted(LL)	#ordena LL de menor a mayor; resulto ser mas efectivo
	#for i in L:	print(i)
	#print("")
	#normalizamos las listas de ratios para que coincidan las "figuras"
	for k in range(1,len(L)):
		dd=len(L[k])
		m=0
		#calculamos la media de las proporciones entre ratios de golpes para "cada referenciacion" (cada lista de  L)
		for kk in range(dd):
			m+=L[k][kk]/L[k-1][kk]/dd
		mm=round(ro*m)/ro	#la redondeamos para normalizar
		#print(mm)
		L[k]=[q/mm for q in L[k]]	#modificamos la lista en analisis de forma que la siguiente tome a esta (modificada como referencia)
						#entonces todo quedara normalizado respeco la primera lista (la de ratios menores)
						#la lista de ratios menores estara referenciada al golpe de mayor duracion
	#print("")
				#[print([round(ro*j)/ro for j in i])for i in L]
	#print("")
	#for k in L:	print(k)
	#print("")
	#cada normalizacion esta hecha para cada referenciacion (ver lista LL), por lo que seran diferentes
	#hacemos la media de las normalizaciones y redondeamos
	#definimos el numero de la "mayor" figura
	#N=2
	return [N*round(ro*sum([i[j] for i in L])/len(L))/ro for j in range(len(L[0]))]


PIN=Pin(5,Pin.IN)	#PIN.value()
LED=Pin(16,Pin.OUT)	#PIN.on() PIN.off()

T=[]
b=""
#bucle recoge golpes
while b=="":
	b=input("...")	#insertar cualquier valor para parar
	T.append(ticks_ms())	#time.ticks_ms()

print(analisis(T,4,2))
