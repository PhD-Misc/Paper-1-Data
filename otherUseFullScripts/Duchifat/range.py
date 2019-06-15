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
line1 = "DUCHIFAT"
line2 = "1 40021U 14033M   16080.72630360  .00001579  00000-0  17313-3 0  9990"
line3 = "2 40021  97.9377 347.0557 0013429   0.3746 359.7479 14.89116495 95096"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level

range_array = np.zeros(40)
waterfall=np.zeros((90, 768))

for timeStep in range(40):
	timeStep+=25
	print("working on timestep " +str(timeStep))
	for f in range(1):
		print("Frequency channel " + str(f))
		hud1 = fits.open('1142521608-2m-' + str(timeStep) + '-' + str(f).zfill(4)+ '-image.fits')
		hud2 = fits.open('1142521608-2m-' + str(timeStep+1) + '-' + str(f).zfill(4)+ '-image.fits')

		header1 = hud1[0].header
		header2 = hud2[0].header
		
		wcs1 = WCS(header1, naxis=2)
		wcs2 = WCS(header2, naxis=2)

		UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1.25)
		

		#The below section calculates the position of the satellite in the top image in the cooridnate system of the top image



		#The below section calculates the position of the satellite in the top image in the coordinates sytem o fhte top image
		mwa.date = UTCTime2
		sat.compute(mwa)
		#print("making diff images")
		#The below section calculates the diff image 2D array
		range_array[timeStep-25] = sat.range
		
print("max is " + str(np.max(range_array)))
print("min is " + str(np.min(range_array)))



