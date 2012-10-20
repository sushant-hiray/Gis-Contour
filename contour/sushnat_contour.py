from numpy import matrix
from numpy import *
from numpy.linalg import *
from numpy.matrix import * 
from reading-dat
# input: latlon: N*2 ndarray (N : no of points whose elevation is known), N*1 ndarraya, a ,b : dimensions of the grid)
# n=N, 

latlon= .....
elevations=....


st_lat=...
st_lon=...

temp_lat=st_lat
temp_lon=st_lon


grid=zeros(a,b,3)

a=int(input("Enter a"))
b=int(input("Enter b"))

#grid_width in degrees
lat_grid_width= 5/111000

lon_grid_width=5/111321


def variogram(x1,x2):
	return norm(x1-x2) #change it later - should satisfy variogram(x,x)=0


#: initialising array A 

s=(n+1,n+1)
A=zeros(s)
for i in range(n):
	for j in range(n):
		A[i][j]=-variogram(latlon(i),latlon(j))

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
		grid[a][b]=[temp_lon,temp_lat,res[;n+1].T * elevations]
		temp_lon+=lon_grid_width
		
	
	temp_lat+=lat_grid_width	
	temp_lon=start_lon	
				


		
