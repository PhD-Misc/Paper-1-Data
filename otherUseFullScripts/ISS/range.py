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
from astropy.nddata import Cutout2D
import math



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

range_array = np.zeros(30)
waterfall=np.zeros((90, 768))

for timeStep in range(30):
	print("working on timestep " +str(timeStep))
	for f in range(1):
		print("Frequency channel " + str(f))
		hud1 = fits.open('1142425368-2m-' + str(timeStep) + '-' + str(f).zfill(4)+ '-image.fits')
		hud2 = fits.open('1142425368-2m-' + str(timeStep+1) + '-' + str(f).zfill(4)+ '-image.fits')


		##The below section is used to add noise
		
		##### Noise section ends herer


		header1 = hud1[0].header
		header2 = hud2[0].header
		
		wcs1 = WCS(header1, naxis=2)
		wcs2 = WCS(header2, naxis=2)

		UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=-0.5)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=0)
		

		#The below section calculates the position of the satellite in the top image in the cooridnate system of the top image



		#The below section calculates the position of the satellite in the top image in the coordinates sytem o fhte top image
		mwa.date = UTCTime2
		sat.compute(mwa)
		range_array[timeStep] = sat.range
		print("The range is "  + str(sat.range))
		#np.savetxt("noiseTest-" + str(timeStep) + ".txt", waterfall[timeStep,:])
print("max is " + str(np.max(range_array)))
print("min is " + str(np.min(range_array)))

plt.imshow(waterfall, cmap=plt.cm.viridis, interpolation='bilinear', aspect='auto')
plt.colorbar()
plt.show()



