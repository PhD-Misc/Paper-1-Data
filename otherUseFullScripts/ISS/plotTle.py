from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import numpy as mp
import astropy
from astropy.wcs import WCS
import ephem
import time
from datetime import datetime, timedelta
from array import *
import os.path
import math
from astropy.nddata import Cutout2D


#The below section is the TLE date of the satellite
line1 = "ISS"
line2 = "1 25544U 98067A   16078.18872957  .00011987  00000-0  18767-3 0  9997"
line3 = "2 25544  51.6438 151.8661 0001598 315.1341 138.1171 15.54181702990822"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level

freq = [389, 427, 429, 489, 519, 524, 534, 538, 540, 554, 564, 594, 597, 614, 634, 674, 684, 691, 692, 694, 714, 729, 739, 740, 748, 749, 754, 759, 762]

data1 = np.zeros((1400, 1400))
data2 = np.zeros((1400,1400))

timestep=56
#714
#684
#674
#634
for f in freq:
	f=674	
	hdu1 = fits.open('1142425368-2m-' +str(timestep) + '-' + str(f).zfill(4)+ '-image.fits')
	data = hdu1[0].data[0,0,:,:]
	data1+=data

for f in freq:
        f=674
	hdu2 = fits.open('1142425368-2m-' +str(timestep+1) + '-' + str(f).zfill(4)+ '-image.fits')
        data = hdu2[0].data[0,0,:,:]
        data2+=data

length = len(freq)
dataDiff = data2 - data1
newData = [ x/length for x in dataDiff]
header = hdu2[0].header
UTCtime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S') +timedelta(seconds=0)
mwa.date = UTCtime


wcs = WCS(hdu2[0].header, naxis=2)
plt.figure().add_subplot(1,1,1, projection=wcs)
plt.imshow(newData,  cmap=plt.cm.inferno)
f = open('tle.txt')
line = f.readline()
counter = 1
line1 = 'SATELLITE'
while line:
	if counter%2 ==1:
		line2=line
	else:
		line3=line
		sat=ephem.readtle(str(line1), str(line2),str(line3))
		sat.compute(mwa)
		x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
		if (0 <= x < 1400) and (0 <= y < 1400):
			plt.plot(x,y, marker='o', color='yellow', markeredgecolor='black', markersize=5)
	print('reading line ' +str(counter))
	counter += 1
	line = f.readline()
plt.grid(linestyle='--', color='black')
plt.xlabel("x pixels(RA)")
plt.ylabel("y pixels(Dec)")
plt.show()





