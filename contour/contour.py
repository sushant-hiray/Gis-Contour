#!C:/Python27/python
# enable debugging
import json
import urllib2

import string, sys, os

import matplotlib

import matplotlib.pyplot as plt
from grid_kriging import *

#Use this if you know all the two corners

#samp_rate = area/no of points you require

'''
st_lat = float(sys.argv[1])
st_lon = float(sys.argv[2])
end_lat = float(sys.argv[3])
end_lon = float(sys.argv[4])
samp_rate = float(sys.argv[5])
pathtrue=sys.argv[6]
samp_rate = samp_rate*0.009'''

#Use this if you know only the latlon of the centre

c_lat = float(sys.argv[1])
c_lon = float(sys.argv[2])
area = float(sys.argv[3])
samp_rate = float(sys.argv[4])
pathtrue=sys.argv[5]

#diff: width of the rectangle in degrees
diff= area* 0.0045 

st_lat = c_lat - diff
st_lon = c_lon - diff
end_lat = c_lat + diff
end_lon = c_lon + diff
samp_rate = samp_rate*0.009

f3 = open(pathtrue+"_bound.txt", 'w')
f3.write(str(st_lat)+" "+str(st_lon)+"\n"+str(end_lat)+" "+str(end_lon))
f3.close()



LAT = c_lat
LON = c_lon
d_lat = (end_lat-st_lat)
d_lat_in_deg = d_lat/(10**5)
d_lon = (st_lon-end_lon)
d_lon_in_deg = d_lon/(10**5)



nosas_lat = int(d_lat/samp_rate) + 1
nosas_lon = int(d_lon/samp_rate) + 1
start_lat = st_lat
start_lon = st_lon


f2=open("proxies.txt")
proxy_url=f2.readline()



k=0
location_str = ''
path=pathtrue+'.txt'
f = open(path, 'w')
latitude= []
longitude= []
for i in range(nosas_lon):
    lg = start_lon + samp_rate * i
    longitude.append(lg)
for i in range(nosas_lat):
    lt = start_lat + samp_rate * i
    latitude.append(lt)
for i in range(nosas_lat):
    lt = start_lat + samp_rate * i
    for j in range(nosas_lon):
        lg = start_lon + samp_rate * j
        location_str = location_str + str(lt) + ',' + str(lg) + "|"
        k = k + 1
        if(k==25 or (i==(nosas_lat-1) and j==(nosas_lon-1))):
            url =  "http://maps.googleapis.com/maps/api/elevation/json?locations=" + location_str
            url = url.rstrip('|') + "&sensor=false"
            if len(proxy_url)!=0:
                proxy=urllib2.ProxyHandler({'http': proxy_url})
                auth = urllib2.HTTPBasicAuthHandler()
                opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
                urllib2.install_opener(opener)
            a = urllib2.urlopen(url)			
            p = json.load(a)
            results = p['results']
            length = len(results)
            e = []
            lat = []
            lng = []
            for kk in range(length):
                e.append(results[kk]['elevation'])
                latlng = results[kk]['location']
                lat.append(latlng['lat'])
                lng.append(latlng['lng'])
	    for kk in range(length):
                tstr=str(lng[kk])+'\t'+str(lat[kk])+'\t'+str(e[kk])
                for i in range(len(tstr)):
                    if(tstr[i]!=' 'and tstr[i]!='\t'and tstr[i]!='\n'):
                        lflg=1
                if(lflg==1):
                    f.write(str(lng[kk])+'\t'+str(lat[kk])+'\t'+str(e[kk])+'\n')
                lflg=0
                
	    k=0
	    location_str = ''

f.close()
x = loadtxt(pathtrue+'.txt')

X_min = min(x[:,0]); X_max = max(x[:,0]); Y_min = min(x[:,1]); Y_max = max(x[:,1])
X = arange(X_min,X_max,(X_max-X_min)/50);	X = append(X,X_max)
Y = arange(Y_min,Y_max,(Y_max-Y_min)/50);	Y = append(Y,Y_max)
Z = grid_kriging(x[:,0:2],x[:,2],X,Y)

CS=plt.contour(X, Y, Z, 50)
plt.axis('off')
plt.clabel(CS, fontsize=3, inline=1, linewidth=3, edgecolor='w')
plt.savefig(pathtrue+".png",dpi=1000,transparent=True,bbox_inches='tight')

