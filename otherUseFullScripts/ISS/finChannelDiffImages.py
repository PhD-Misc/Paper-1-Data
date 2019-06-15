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

hfont = {'fontname':'Helvetica', 'size':12}

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


for timestep in range(90):
	print("working on timestep " +str(timestep))
	data1 = np.zeros((1400,1400))
	data2 = np.zeros((1400,1400))
	freq = [389, 427, 429, 489, 519, 524, 534, 538, 540, 554, 564, 594, 597, 614, 634, 674, 684, 691, 692, 694, 714, 729, 739, 740, 748, 749, 754, 759, 762]
	for f in freq:
		hud = fits.open('1142425368-2m-' +str(timestep) + '-' + str(f).zfill(4)+ '-image.fits')
		data = hud[0].data[0,0,:,:]
		data1+=data;
	for f in freq:
                hud = fits.open('1142425368-2m-' +str(timestep+1) + '-' + str(f).zfill(4)+ '-image.fits')
                data = hud[0].data[0,0,:,:]
                data2+=data;
	length = len(freq)
	dataDiff = data2-data1
	print("The length is " +str(length))
	newData = [ x/length for x in dataDiff]
	plt.imshow(newData)

	plt.colorbar()
	plt.savefig('diffImage' +str(timestep) + '.png')
	plt.clf()

		
