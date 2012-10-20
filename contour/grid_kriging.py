"""
The function grid_kriging requires four arguments.
1). observation locations in terms of 'x', an Nx2 numpy array (ndarray), of lats,longs of N locations
2). corresponding elevations in terms of 'y', a 1-dim ndarray of size N
3). X-coordinates of locations of the desired grid in terms of 'X', a 1-dim ndarray (of size p, say).
4). Y-coordinates of locations of the desired grid in terms of 'Y', a 1-dim ndarray (of size q, say).
The return value is a 2-dim ndarray Z having shape pxq, of interpolated elevation values for the pxq desired grid-points(locations).
"""

from numpy import *
from numpy.linalg import *

def variogram(x,y):
	N = shape(y)[0]
	k = 0
	temp_v = zeros((2,N*(N-1)/2))
	for i in range(N):
		for j in range(i+1,N):
			temp_v[0,k] = norm(x[i]-x[j])
			temp_v[1,k] = 0.5 * (y[i]-y[j])**2
			k = k + 1
	d_min = min(temp_v[0]);	d_max = max(temp_v[0])
	total_range = d_max - d_min
	X = zeros(N);	Y = zeros(N);	Z = zeros(N)
	for i in range(N*(N-1)/2):
		if(temp_v[0,i] != d_max):
			index = floor(((temp_v[0,i]-d_min)/total_range)*(N))
		else:
			index = N - 1
		X[index] = X[index] + temp_v[0,i];		Y[index] = Y[index] + temp_v[1,i];		Z[index] = Z[index] + 1
	v = zeros((2,N))
	for i in range(N):
		if(Z[i]==[0]):
			continue
		else:
			v[0,i] = X[i]/Z[i];			v[1,i] = Y[i]/Z[i]
	return v

def grid_kriging(x,y,X,Y):
	""" hi """
	v_empirical = variogram(x,y);	v_model = polyfit(v_empirical[0],v_empirical[1],1)
	N = len(y);	K = zeros((N+1,N+1))
	for i in range(N):
		for j in range(i,N):
			K[i,j] = K[j,i] = -(v_model[0] + v_model[1]*norm(x[i]-x[j]))
	K[N,:] = 1;	K[:,N] = 1;	K[N,N] = 0
	k = append(y,0)
	eta = dot(inv(K),k)
	Z = zeros((len(X),len(Y)))
	for i in range(len(X)):
		for j in range(len(Y)):
			diff_vec = array([X[i]-x[:,0],Y[j]-x[:,1]]).T
			dist_vec = zeros(N)
			for s in range(N):
				dist_vec[s] = norm(diff_vec[s,:])
			Vario = v_model[0] + v_model[1]*dist_vec
			Vario = append(-Vario, 1)
			Z[i,j] = dot(eta,Vario)
	Z1=transpose(Z)
	return Z1
