## MCE para medidas ZFC a partir de los datos sin exportar del VSM Quantum Design - VersaLab
## Por: Rodrigo Toraño Valle
## python 3

import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from scipy.interpolate import splrep,BSpline
from scipy.integrate import cumtrapz
from tkinter.filedialog import askopenfilenames
Tk().withdraw()	#avoid root window
from scipy.signal import find_peaks

def zfc(T,M):
	## Extraer ZFC (opcional)
	pks=np.concatenate(([0,find_peaks(T)[0],-1]),axis=None)
	return T[pks[0]:pks[1]],M[pks[0]:pks[1]]

def ifsorted(L):
	## Ordena campos (Hs) y crea lista (HSI) de posiciones respecto H (desordenada)
	LSI=[]
	Ls=sorted(L)	#Campos ordenados
	for i in range(len(L)):
		LSI.append(L.index(Ls[i]))
	return LSI

def errfilter(E,errmin):
	## Devuelve posiciones de los errores superiores a val
	return [i for i in range(len(E)) if E[i]>errmin]

filepaths=askopenfilenames(defaultextension='.DAT',title='Selecciona los ficheros .DAT para los campos deseados',initialdir=os.getcwd())
## NOTA: habría que prohibir la repeticion de campos
H=[]
emes=[]
tes=[]
for path in filepaths:
	#print(path)
	muestra=path.split('/')[-1].split('_')[0]	#Nombre del fichero
	campo=path.split('/')[-1].split('OE')[0].split('_')[-2]
	#campo=path.split('/')[-1][:-4].split('_')[-2]
	print(muestra,campo,'Oe')
	H.append(float(campo)/10000)	#Utilizamos Teslas. NOTA: dejar M en (emu) y dividir por la masa de la muestra en kilogramos para tener unidades de deltaS (J/(Kg*K))
	f=open(path,'r')
	l=f.readlines()
	f.close()
	x=False
	L=[]
	for i in l:
		if '[Data]' in i and not x: x=True
		if x:
			e=i[0:-1].split(',')
			L.append(e)
	L=L[2+1:]
	T=[float(i[2]) for i in L]	#Temperature (K)
	MF=[float(i[3]) for i in L]	#Magnetic Field (Oe)
	M=[float(i[4]) for i in L]	#Moment (emu)
	E=[float(i[5]) for i in L]	#M. Std. Err (emu)
	#[print(T[k],MF[k],M[k],E[k]) for k in range(3)]
	## Maquillar M con E
	#errmin=1
	#M=[(M[j-1]+M[j+1])/2 for j in[i for i in range(1,len(E)-1) if E[i]>errmin]]	#sustituye los momentos con errores superiores a errmin con valores medios
	T,M=zfc(T,M)
	emes.append(M)
	tes.append(T)
		
## Ordenar campos y detrminar restricción en temperatura de trabajo
HSI=ifsorted(H)
H=sorted(H)
hh=len(H)
tbot=max([i[0] for i in tes])
ttop=min([i[-1] for i in tes])
#tbot=80.
#ttop=160.

## Interpolación mediante spline cúbico k=3
Kpaso=1	#(K/paso)
Tspline=np.linspace(tbot,ttop,int((ttop-tbot)/Kpaso))
tt=len(Tspline)
mmda=[]
for i in HSI:
	(t,c,k)=splrep(tes[i],emes[i],s=0,k=3)
	spline=BSpline(t,c,k,extrapolate=True)
	#plt.plot(tes[i],emes[i],'o',Tspline,spline(Tspline),'+')#,t,c,'x'
	mmda.append(spline(Tspline))
#plt.show()

## Conformar matrices de datos
ttda=np.transpose(np.array([Tspline for i in HSI]))		#tt*hh
mmda=np.transpose(np.array(mmda))				#tt*hh
hhda=np.array([H for i in range(tt)])				#tt*hh

print('(tt,hh)=(%i,%i)'%(tt,hh),np.shape(mmda),np.shape(ttda),np.shape(hhda),sep='\n')
#input('***')
#plt.plot(ttda,mmda,'o')
#plt.show()

#input('M')
font = {'family': 'arial',
        'size': 24,
        }
plt.rc('font', **font)
fig=plt.subplot(111)
for i in range(hh-1,-1,-1):
	plt.plot(ttda[:,i],mmda[:,i],'o',label='%i Oe'%(H[i]*10000))

plt.title('$m$ vs $T$')
plt.xlabel('$T$ (K)')
plt.ylabel('$m$ (emu)')
box=fig.get_position()
fig.set_position([box.x0,box.y0,box.width*0.8,box.height])
fig.legend(loc='center left',bbox_to_anchor=(1,0.5),prop={'size': 20})
plt.subplots_adjust(left=0.1,right=0.8)
plt.show()

## DeltaS (temperature derivative of the magnetization = dxdc)
x=mmda	#defining of the matrix x (tt*hh)
c=ttda	#defining la variable c (tt*hh)
dxdc=np.zeros((tt,hh))
for j in range(hh):
	dxdc[0,j]=(x[1,j]-x[0,j])/(c[1,j]-c[0,j])
for i in range(1,tt-1):
    for j in range(hh):
        dxdc[i,j]=0.5*(((x[i+1,j]-x[i,j])/(c[i+1,j]-c[i,j]))+((x[i,j]-x[i-1,j])/(c[i,j]-c[i-1,j])))
for j in range(hh):
	dxdc[tt-1,j]=(x[tt-1,j]-x[tt-2,j])/(c[tt-1,j]-c[tt-2,j])

## DeltaS according to Maxwell Relationship MR (jj*tt)
ss=np.zeros((hh,tt))
dH=np.transpose(np.concatenate((np.zeros((tt,1)),hhda),axis=1))
dMdT=np.transpose(np.concatenate((np.zeros((tt,1)),dxdc),axis=1))
for i in range(tt):
    ss[:,i]=cumtrapz(dMdT[:,i],dH[:,i])
ss=ss.transpose()

#plt.plot(ttda,ss,'o')
#plt.show()

mov=0.015e-3 ## masa o volumen de la muestra

Kpaso=0.1	#(K/paso)
tbot=80.
ttop=160.
Tspline=np.linspace(tbot,ttop,int((ttop-tbot)/Kpaso))
ssf=[]
for i in HSI:
	(t,c,k)=splrep(ttda[:,i],ss[:,i],s=0,k=3)
	spline=BSpline(t,c,k,extrapolate=True)
	ssf.append(spline(Tspline))

ttdaf=np.transpose(np.array([Tspline for i in HSI]))		#tt*hh
ssf=np.transpose(np.array(ssf))/mov				#tt*hh

#input('deltaS')

fig=plt.subplot(111)
plt.plot(ttdaf[ssf==ssf.max()],ssf[ssf==ssf.max()],'o',label='$\Delta S_{max}$=%.2f'%ssf.max())
for i in range(hh-1,-1,-1):
	plt.plot(ttdaf[:,i],ssf[:,i],'-',label='%i Oe'%(H[i]*10000))

plt.title('MCE')
plt.xlabel('$T$ (K)')
plt.ylabel('$\Delta S$ (J $kg^{-1}$ $K^{-1})$')
box=fig.get_position()
fig.set_position([box.x0,box.y0,box.width*0.8,box.height])
fig.legend(loc='center left',bbox_to_anchor=(1,0.5),prop={'size': 20})
plt.subplots_adjust(left=0.1,right=0.8)
plt.show()
#################################################################################################################
mxs=[max(ssf[:,i]) for i in range(hh)]
fig=plt.subplot(111)
plt.plot(H,mxs,'o')

plt.title('$\Delta S$ vs $H$')
plt.xlabel('$H$ (T)')
plt.ylabel('$\Delta S$ (J $kg^{-1}$ $K^{-1})$')
box=fig.get_position()
fig.set_position([box.x0,box.y0,box.width*0.8,box.height])
plt.subplots_adjust(left=0.1,right=0.8)
plt.show()

save=input('SAVE? (y/n)').lower()
if save=='y':
	np.savetxt(muestra+'_hhda.csv',hhda,delimiter=',')
	np.savetxt(muestra+'_ttda.csv',ttda,delimiter=',')
	np.savetxt(muestra+'_mmda.csv',mmda,delimiter=',')
	np.savetxt(muestra+'_deltaS.csv',ss,delimiter=',')
	np.savetxt(muestra+'_dxdc.csv',dxdc,delimiter=',')
print('Fin')
