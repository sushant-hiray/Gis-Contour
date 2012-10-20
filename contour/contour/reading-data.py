from numpy import *
from numpy.linalg import *

f = open('Desktop.txt', 'r')

size=(120,3)

print f
Data = zeros(size)
s=f.readline()
i=0

while(s != ""):
	k=s.split()
	Data[i][0]=float(k[0])
	Data[i][1]=float(k[1])
	Data[i][2]=float(k[2])
	i = i+1
	s=f.readline()
	
