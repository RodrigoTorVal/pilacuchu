import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
import peakutils as pk
D=[]
for d in range(20,260,20):
	F=[]
	for fi in range(1,6):
		print("Apertura: %dum\nFichero: %d"%(d,fi))
		path="/home/rodrigo/Desktop/FAM-PL-LIBS/Archivos Práctica LIBS/FWHM vs Anchura Rendija/Red 1200 lineas por mm/"
		f=open(path+"Apertura_%dum_%d.asc"%(d,fi),"r")
		L=f.readlines()
		f.close()
		V=[[float(j) for j in i[:-1].split(",")] for i in L]
		lo=np.array([i[0] for i in V])
		cc=np.array([i[1] for i in V])
		#pki=pk.indexes(cc, thres=0.333, min_dist=1)
		#interp_pki=pk.interpolate(lo,cc,ind=pki)
		#print(interp_pki)
		lo_interp=np.linspace(lo[0],lo[-1],100000)
		#cc_interp=np.interp(lo_interp,lo,cc)
		cc_interp=spline(lo,cc,lo_interp)
		pkii=pk.indexes(cc_interp, thres=0.333, min_dist=1)
		print("#picos: %d"%len(pkii))
		#print(lo_interp[pkii])
		#los picos tienen un ancho total aproximado de 1 nm
		#aproximamos la mitad de posiciones necesariar para conseguir esa anchura
		pni=1
		delta_lo=0
		while delta_lo<0.5:
			delta_lo=lo_interp[pni]-lo_interp[0]
			pni+=1

		fwhm=[]
		for i in pkii:
			lo1=lo_interp[i-pni:i+pni]
			cc1=cc_interp[i-pni:i+pni]
			max_cc1=max(cc1)
			fwhmi=[i for i in range(len(cc1)) if cc1[i]>(max_cc1-min(cc))/2.]
			fwhm.append([lo_interp[i],lo1[max(fwhmi)]-lo1[min(fwhmi)]])
			print([lo_interp[i],lo1[max(fwhmi)]-lo1[min(fwhmi)]])
			#plt.plot(lo1[[min(fwhmi),max(fwhmi)]],cc1[[min(fwhmi),max(fwhmi)]],'--k')

		"""fig=plt.figure()
		timer=fig.canvas.new_timer(interval=3000)
		timer.add_callback(plt.close)
		plt.plot(lo_interp,cc_interp,'-b',lo_interp[pkii],cc_interp[pkii],'xr')
		plt.xlabel("Longitud de onda")
		plt.ylabel("Cuentas")
		timer.start()
		plt.show()"""
		
		F.append(fwhm)
	D.append([d,F])
ff=open("datos.dat","w")
ff.write("D="+str(D))
ff.close()
