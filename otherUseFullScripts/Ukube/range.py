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
line1 = "UKUBE"
line2 = "1 40074U 14037F   16079.81203031  .00001270  00000-0  16363-3 0  9993"
line3 = "2 40074  98.3348 169.0455 0005943  80.4298 279.7595 14.82938013 91827"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


waterfall=np.zeros((90, 768))
range_array = np.zeros(10)

for timeStep in range(10):
	timeStep+=5
	print("working on timestep " +str(timeStep))
	for f in range(1):
		print("Frequency channel " + str(f))
		hud1 = fits.open('1142351440-2m-' + str(timeStep) + '-' + str(f).zfill(4)+ '-image.fits')
		hud2 = fits.open('1142351440-2m-' + str(timeStep+1) + '-' + str(f).zfill(4)+ '-image.fits')

		header1 = hud1[0].header
		header2 = hud2[0].header
		
		wcs1 = WCS(header1, naxis=2)
		wcs2 = WCS(header2, naxis=2)

		UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1.75)
		

		#The below section calculates the position of the satellite in the top image in the cooridnate system of the top image

		mwa.date = UTCTime2
		sat.compute(mwa)
		range_array[timeStep-5] = sat.range

print("max is " + str(np.max(range_array)))
print("min is " + str(np.min(range_array)))



