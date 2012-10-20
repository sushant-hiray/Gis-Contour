from numpy import matrix
from numpy import *
from numpy.linalg import *
#from numpy import matrix
from numpy import linalg


import math
import cmath



n=110


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
	

# input: latlon: N*2 ndarray (N : no of points whose elevation is known), N*1 ndarraya, a ,b : dimensions of the grid)
# n=N, 


latlon= Data[: n][: 2]
latlong=[]
for i in range(n):
	latlong.append([Data[i][0],Data[i][1]])
elevations=Data[: n][2]


st_lat=Data[0][0]
st_lon=Data[0][1]

temp_lat=st_lat
temp_lon=st_lon


a=20
b=20

s=(a,b)
grid=zeros(s)


#grid_width in degrees
lat_grid_width= 5/111000

lon_grid_width=5/111321


def variogram(x1,x2):   #should satisfy variogram(x,x)=0\
	l=50/111000          # range, parameter of the exponential variogram
	h=((x1[0]-x2[0])**2 + (x1[1]-x2[1])**2)**0.5
	return (1-exp(h/l))     

#: initialising array A 

s=(n+1,n+1)
A=zeros(s)
for i in range(n):
	for j in range(n):
		A[i][j]=-variogram(latlong[i],latlong[j])

A[n]=ones(n+1)
A[n][n]=0
	
#*****************end of initialisation************************

#inverse of A

A_inv=A.I

#:kriging masala 
for i in range(a):
	
	for j in range(b):
		t=ones(n+1,1)
		
		for k in range(n):
			t[k]=-variogram([temp_lat,temp_lon],latlong(k))
		
		res=A_inv*t	
		grid[a][b]=[temp_lon,temp_lat,res[:n+1].T * elevations]
		temp_lon+=lon_grid_width
		
	
	temp_lat+=lat_grid_width	
	temp_lon=start_lon	
				


		
