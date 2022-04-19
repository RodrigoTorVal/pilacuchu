import os
os.system("ls > ls.txt")
f=open("ls.txt","r")
N=len(f.readlines())
f.close()

L=[]
f=open("ls.txt","r")
for i in range(N):
	rl=f.readline()[:-1]
	if rl!="ls.txt" and rl!="comma2points.py": L.append(rl)
f.close()

#print(L)

for k in L:
	fi=open(k,"r")
	lines=fi.readlines()
	fi.close()
	fo=open("c2p_"+k,"w")
	for kk in lines:
		splt=kk.split(",")
		c2p=splt[0]
		for kkk in splt[1:]:
			c2p=c2p+"."+kkk
		fo.write(c2p)
	fo.close()
