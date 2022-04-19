CR=int(input("Radio Creativo: "))
CRx=int(input("coordenada central X: "))
CRy=100
CRz=int(input("coordenada central Z: "))
print("/gamemode 0 @a[y=%d,x=%d,z=%d,m=1,rm=%d]"%(CRy,CRx,CRz,CR))
print("/clear @a[y=%d,x=%d,z=%d,r=%d,rm=%d]"%(CRy,CRx,CRz,CR+5,CR))
print("/effect @a[y=%d,x=%d,z=%d,m=0,r=%d,rm=%d] 2 1 255"%(CRy,CRx,CRz,CR+5+7,CR-7))
print("/tell @a[y=%d,x=%d,z=%d,m=0,r=%d,rm=%d] Estás entrando en lazona creativa, lo perderás todo."%(CRy,CRx,CRz,CR+5+7,CR+5))
print("/tell @a[y=%d,x=%d,z=%d,m=0,r=%d,rm=%d] Estás saliendo de la zona creativa, lo perderás todo."%(CRy,CRx,CRz,CR,CR-5))
