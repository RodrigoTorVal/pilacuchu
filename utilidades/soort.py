L=[123,6,76767,545,33,6,1,0,-1]
print(L)
for x in range(len(L)):
	for y in range(len(L)-1):
		if L[y]>L[y+1]:
			h=L[y+1]
			L[y+1]=L[y]
			L[y]=h
print(L)
