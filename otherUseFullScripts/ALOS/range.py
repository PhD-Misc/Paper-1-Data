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
line1 = "ALOS"
line2 = "1 28931U 06002A   16079.98024251 +.00000391 +00000-0 +86490-4 0  9999"
line3 = "2 28931 097.8961 122.7695 0001002 052.8253 307.3040 14.62149601541084"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


waterfall=np.zeros((90, 768))
range_array = np.zeros(25)
for timeStep in range(25):
	print("working on timestep " +str(timeStep))
	for f in range(1):
		print("Frequency channel " + str(f))
		hud1 = fits.open('1142340880-2m-' + str(timeStep) + '-' + str(f).zfill(4)+ '-image.fits')
		hud2 = fits.open('1142340880-2m-' + str(timeStep+1) + '-' + str(f).zfill(4)+ '-image.fits')

		header1 = hud1[0].header
		header2 = hud2[0].header
		
		wcs1 = WCS(header1, naxis=2)
		wcs2 = WCS(header2, naxis=2)

		UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)
		

		#The below section calculates the position of the satellite in the top image in the cooridnate system of the top image



		#The below section calculates the position of the satellite in the top image in the coordinates sytem o fhte top image
		mwa.date = UTCTime2
		sat.compute(mwa)
		range_array[timeStep] = sat.range
print("max is " + str(np.max(range_array)))
print("min is " + str(np.min(range_array)))



