import random

class tab:
	"""Tablero tres en raya"""
	def __init__(self):
		self.T=[0,"1","2","3","4","5","6","7","8","9"]
		self.libres=[]
	def salida(self):
		return ".........................\n:	:	:	:\n:   %s   :   %s   :   %s   :\n\
:	:	:	:\n:.......:.......:.......:\n:	:	:	:\n:   %s   :   %s   :   %s   :\n\
:	:	:	:\n:.......:.......:.......:\n:	:	:	:\n:   %s   :   %s   :   %s   :\n\
:	:	:	:\n:.......:.......:.......:" \
%(self.T[1],self.T[2],self.T[3],self.T[4],self.T[5],self.T[6],self.T[7],self.T[8],self.T[9])

	def limpia(self):
		self.T=[0," "," "," "," "," "," "," "," "," "]
	def pon(self,pos,sign):
		if pos>0 and pos<10:
			self.T[pos]=sign
	def raya(self):
		P=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
		estado=""
		self.libres=[i for i,j in enumerate(self.T) if j==" "]
		if len(self.libres)==0:
			estado="empate"
		for k in P:
			if self.T[k[0]]==self.T[k[1]] and self.T[k[2]]==self.T[k[0]] and self.T[k[0]]!=" ":
				estado=self.T[k[0]]
		return estado



def IA(T,A="O",B="X"):
	"""Inteligencia Artificial"""
	tabIA=tab()
	#gano?
	sel=[]
	for n,i in enumerate(T):
		if i==" ":
			tabIA.T=T[:]
			tabIA.pon(n,A)
			if tabIA.raya()==A:
				sel.append(n)
	if len(sel)==0:
		#gana?
		for n,i in enumerate(T):
			if i==" ":
				tabIA.T=T[:]
				tabIA.pon(n,B)
				if tabIA.raya()==B:
					sel.append(n)
		if len(sel)==0:
			#gano luego?
			for n,i in enumerate(T):
				if i==" ":
					tabIA.T=T[:]
					tabIA.pon(n,A)
					T2=tabIA.T[:]
					ch2=[]
					for nn,j in enumerate(tabIA.T):
						if j==" ":
							tabIA.T=T2[:]
							tabIA.pon(nn,A)
							if tabIA.raya()==A:
								ch2.append(nn)
					if len(ch2)>1:
						sel.append(n)
			if len(sel)==0:
				tabIA.T=T[:]
				cf=[]
				cB=[]
				cA=[]
				for n,i in enumerate(T):
					if i==" ": cf.append(n)
					if i==B: cB.append(n)
					if i==A: cA.append(n)
				if len(cf)==9: sel=[1,3,7,9]
				elif (1 in cB) or (3 in cB) or (7 in cB) or (9 in cB):
					if 5 in cf: sel=[5]
					elif 5 in cB:
						sel=[j for j in cf if j in [1,3,7,9]]
						if len(sel)==0: sel=cf
					else:
						sel=[j for j in cf if j in [2,4,6,8]]
						if len(sel)==0: sel=cf
				else:
					for j in cf:
						if j in [1,3,7,9]: sel.append(j)
					if len(sel)==0:
						for j in cf:
							if j in [5]: sel.append(j)
						if len(sel)==0: sel=cf
	return sel

def cosa(n):
	if n in

tabla=tab()
tabla.limpia()
CPU=random.choice([True,False])

if CPU:
	rsel=random.choice(IA(tabla.T[:]))
	tabla.pon(rsel,"O")
	N=1
else:
	M=random.choice(IA(tabla.T[:]))
	tabla.pon(M,"X")
	N=0

while True:
	print(tabla.salida())
	tabla.libres=[i for i,j in enumerate(tabla.T) if j==" "]
	estado=tabla.raya()
	if estado!="":
		print(estado)
		break
	N=N+1
	if N%2==0:
		M=random.choice(IA(tabla.T[:],"X","O"))
		tabla.pon(M,"X")
	else:
		rsel=random.choice(IA(tabla.T[:],"O","X"))
		tabla.pon(rsel,"O")
