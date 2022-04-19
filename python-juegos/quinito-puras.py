from random import randrange,choice,seed

def printif(x):
	print(x)
	return None

class Cachi:
	"""El Cachi"""
	def __init__(self,nombre,vasoscachi):
		self.sustancia=vasoscachi
		self.nombre=nombre
		self.nombrey="%s (%s)"%(self.nombre,self.sustancia)
	def bebe(self,vasos):
		printif("%s bebe %d"%(self.nombre,vasos))
		if self.sustancia>vasos:
			self.sustancia-=vasos
			self.nombrey="%s (%s)"%(self.nombre,self.sustancia)
		else:
			self.sustancia=0
			self.nombrey="%s (%s)"%(self.nombre,self.sustancia)

def jugar(semilla=None):
	#seed(semilla)
	tirada=[randrange(1,7),randrange(1,7)]
	return tirada

def valj(jugada):
	"""Asigna valor a jugadas en formato [dado1,dado2]"""
	S=sum(jugada)
	if jugada[0]==jugada[1]:
		return jugada[0]*11
	elif S==11 or S==3:
		return 100
	elif S==4 and jugada[0]!=2:
		return 1000
	else:
		return S

def jesp(jugada):
	"""Detecta jugada especial"""
	S=sum(jugada)
	if S==5 and 1 in jugada:
		return "gato"
	elif S==9 and 4 in jugada:
		return "flaca"
	elif S==11 or S==3:
		return "quinito"
	elif S==4 and jugada[0]!=2:
		return "colindres"
	else:
		return None

def mentir(minimo):
	P=[8,9,10,11,22,33,44,55,66]
	while True:
		manda=input("(Minimo: %d) Mentir con: "%minimo)
		try:
			manda=int(manda)
			if manda>=minimo and manda in P:
				break
		except:
			continue
	return manda

def creencia(minimo,manda):
	d={"s":True,"n":False}
	while True:
		cree=input("Creer (s/n): ")
		if cree=="s" or cree=="n":
			break
	return d[cree]

def percent(p):
	"""Devuelve True 100p veces de 100"""
	if randrange(1,101)>100*p:
		return False
	else:
		return True


CC={8:4/36,9:4/36,10:2/36,11:1/36,22:1/36,33:1/36,44:1/36,55:1/36,66:1/36} #minimo:probabilidad al picar
MM={8:16/36,9:12/36,10:8/36,11:6/36,22:5/36,33:4/36,44:3/36,55:2/36,66:1/36} #minimo:probabilidad al picar
P=[8,9,10,11,22,33,44,55,66,100,1000] #jugadas
J=[Cachi("Puras",24),Cachi("PC",24)] #jugadores
minimo=8
manda=0
n=0
w,we=None,None
br=False #para parar

ss=0
while True:
	if manda!=0: #rutina para creer#####################################
		printif("%s manda %d (Minimo: %d)"%(J[(n)%len(J)].nombrey,manda,minimo))
		n+=1 #avanza cubilete
		if J[n%len(J)].nombre=="Puras":
			#creer=choice([True,False])
			creer=creencia(minimo,manda) #humano cree
		else:
			#creer=percent(CC[manda]) #PC cree
			#creer=percent(MM[minimo]) #PC cree
			if manda<=9:
				creer=choice([True,False])
			else:
				creer=False
		if creer:
			if we:
				printif("%s cree (era %s)"%(J[n%len(J)].nombrey,we))
			else:
				printif("%s cree (era %d)"%(J[n%len(J)].nombrey,w))
			minimo=P[P.index(manda)+1]
		else: #picar
			if we:
				printif("%s pica (era %s)"%(J[n%len(J)].nombrey,we))
			else:
				printif("%s pica (era %d)"%(J[n%len(J)].nombrey,w))
			if manda!=w: #si el anteriror mentia
				printif("Era mentira")
				n-=1 #retrocede cubilete
				if we=="gato": #si es gato
					J[n%len(J)].bebe(2) #bebe 2
				else:
					J[n%len(J)].bebe(1)
				manda,minimo=0,8 #reinicio
				w,we=None,None
			else:  #si pica verdad
				printif("Era verdad")
				if we=="flaca": # si es flaca
					J[n%len(J)].bebe(2) #bebe 2
				else:
					J[n%len(J)].bebe(1)
				manda,minimo=0,8 #reinicio
				w,we=None,None
	#rutina perder######################################################
	for k in J:
		if k.sustancia==0:
			printif("%s pierde"%k.nombrey)
			J.remove(k)
			br=True
	if br and len(J)<=1:
		break
	else:
		br=False
	####################################################################
	ss+=1
	jg=jugar(ss) #tirar para mandar
	w,we=valj(jg),jesp(jg)
	#printif(J[(n)%len(J)].nombre,w)
	#rutina quinito/colindres###########################################
	if we=="quinito" or we=="colindres":
		if we=="quinito":
			vb=2
		if we=="colindres":
			vb=3
		nn=randrange(1,len(J)) #elige victima aleatoria
		n+=nn #manda cubilete
		printif("%s manda %s a %s"%(J[(n-nn)%len(J)].nombrey,we,J[n%len(J)].nombrey))
		ss+=1
		je=jugar(ss) #victima tira dados
		wwe=jesp(je)
		x=1
		while wwe==we: #mientras se devuelva
			vb=vb*2 #se dobla cantidad
			n-=x*nn #devuelve quinito/colindres
			printif("%s devuelve %s a %s"%(J[(n+x*nn)%len(J)].nombrey,we,J[n%len(J)].nombrey))
			ss+=1
			je=jugar(ss) #oponente tira dados
			wwe=jesp(je)
			x=-1*x #para devolver a oponente
		#cuando alguien falla
		printif("%s falla"%J[n%len(J)].nombrey)
		if wwe=="gato": #si devuelve gato
			printif("con un gato...")
			vb=vb*2 #se dobla cantidad
		J[n%len(J)].bebe(vb) #bebe
		n-=x*nn #devuelve cubilete
		#n-=1 #para no pasar cubilete al final del bucle
		manda,minimo=0,8 #reinicio
		w,we=None,None
	####################################################################
	elif minimo==100:
		J[n%len(J)].bebe(1) #bebe
		#n-=1 #para volver a tirar
		manda,minimo=0,8 #reinicio
		w,we=None,None
	elif w<minimo: #mentir
		if J[n%len(J)].nombre=="Puras":
			if we:
				printif("Sacas: %s"%we)
			else:
				printif("Sacas: %s"%w)
			manda=mentir(minimo) #humano miente
		else:
			'''pJugPos=[round(1000*CC[i]/sum([CC[i] for i in P[P.index(minimo):-2]])) for i in P[P.index(minimo):-2]]
			JugPos=[]
			for nu,i in enumerate(P[P.index(minimo):-2]):
				for j in range(pJugPos[nu]):
					JugPos.append(i)
			manda=choice(JugPos) #PCminete siguendo las probabilidades de las jugadas normalizando a las jugadas validas'''
			manda=choice([i for i in P[P.index(minimo):-2]])	#mentira aleatoria
	else:
		manda=w

