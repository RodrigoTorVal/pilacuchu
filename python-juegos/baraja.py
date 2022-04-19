from random import sample,shuffle
class Baraja:
	"""La Baraja"""
	def __init__(self):
		self.baraja=[valor+palu for palu in ['o','c','e','b'] for valor in ['1','2','3','4','5','6','7','S','C','R']]
	def barajar(self):
		shuffle(self.baraja)
	def cortar(self,p):
		return [self.baraja[:p],self.baraja[p:]]
	def coger(self):
		if self.baraja:
			z=self.baraja[0]
			self.baraja=self.baraja[1:]
			return z
		else:
			print('BARAJA TERMINADA')
	def sacar(self,valor,palu):
		pal=['o','c','e','b']
		val=['1','2','3','4','5','6','7','S','C','R']
		sac=[]
		if valor and palu and valor+palu in self.baraja:
			self.baraja.remove(valor+palu)
			sac.append(valor+palu)
		elif valor and not palu:
			for palu in pal:
				if valor+palu in self.baraja:
					self.baraja.remove(valor+palu)
					sac.append(valor+palu)
		elif not valor and palu:
			for valor in val:
				if valor+palu in self.baraja:
					self.baraja.remove(valor+palu)
					sac.append(valor+palu)
		return sac


F=[1,1/2,1/3,2/3,1/4,3/4]
#for frac in F
VVV=0
NNN=0
#frac=1/2
while True:#NNN<100000:
	X=Baraja()
	X.barajar()
	'''
	sac=X.sacar('R',None)
	cort=X.cortar(int(40*(1-frac)))
	cort[1]+=sac
	shuffle(cort[1])
	sinR=cort[0]
	conR=cort[1]
	'''
	mesa=[]
	mano=[]
	while X.baraja:
		A=X.coger()[0]
		#print('... '+A)
		if A in mesa and A!='R':
			mesa.remove(A)
		elif mano and A==mano[-1] and A!='R':
			mano=mano[:-1]
		elif len(mesa)<4:
			mesa.append(A)
		else:
			mano.append(A)
		while mano and len(mesa)<4:
			B=mano[-1]
			if B in mesa and B!='R':
				mesa.remove(B)
			else:
				mesa.append(B)
			mano=mano[:-1]
		#print(mesa)
		#print(mano)#[-1:])
		'''
		if '1' in mesa and not 'R' in mesa:
			NNN-=1
			break
		'''
		if 'R' in mesa and not 'R' in mesa:
			NNN-=1
			break
		if mesa==['R','R','R','R']:
			#print('VICTORIA',X.baraja)
			VVV+=1
			break
	#print('FIN')
	NNN+=1
	print(NNN)
	print(100*VVV/NNN,'%')
	#input('')
