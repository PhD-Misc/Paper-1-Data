from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy.wcs import WCS
import ephem
import time
from datetime import datetime, timedelta
from array import *
import os.path
import math
from astropy.nddata import Cutout2D
from mpl_toolkits.mplot3d import Axes3D



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


cube = np.zeros((1400, 1400, 29))
snr = [None]*90
snrf = [None]*90
for timestep in range(1):
	timestep = 16
	print("working on timestep " +str(timestep))
	data1 = np.zeros((1400,1400))
	data2 = np.zeros((1400,1400))
	freq = [389, 427, 429, 489, 519, 524, 534, 538, 540, 554, 564, 594, 597, 614, 634, 674, 684, 691, 692, 694, 714, 729, 739, 740, 748, 749, 754, 759, 762]
	counter = 0
	for f in freq:
		hud1 = fits.open('1142425368-2m-' +str(15) + '-' + str(f).zfill(4)+ '-image.fits')
		data1 = hud1[0].data[0,0,:,:]
		
	
                hud2 = fits.open('1142425368-2m-' +str(16) + '-' + str(f).zfill(4)+ '-image.fits')
                data2 = hud2[0].data[0,0,:,:]
                
		cube[:,:,counter] = data2-data1	
		counter += 1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


cube = np.ma.masked_where((-180 < cube) & (cube  < 180) , cube)
cmap = plt.cm.viridis
cmap.set_bad(color='blue', alpha=0.5)

X, Y, Z = np.mgrid[:1400,:1400, :29]
ax.scatter(X, Y, Z, c=cube.ravel(), marker = ",")

plt.show()
