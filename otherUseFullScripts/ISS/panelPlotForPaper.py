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

#The below section is the TLE data of the satellite
line1 = "ISS"
line2 = "1 25544U 98067A   16078.18872957  .00011987  00000-0  18767-3 0  9997"
line3 = "2 25544  51.6438 151.8661 0001598 315.1341 138.1171 15.54181702990822"
sat = ephem.readtle(line1, line2, line3)

#The below section sets the MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level



snr_array = np.zeros((768))
numerator_array = np.zeros((768))
denominator_array = np.zeros((768))
for t in range(30):
	t=15
	for f in range(768):
		hdu1 = fits.open("1142425368-2m-" + str(t) + "-" + str(f).zfill(4) + "-image.fits")	
		hdu2 = fits.open("1142425368-2m-" + str(t+1) + "-" + str(f).zfill(4) + "-image.fits")
		print("Working on frequency channel " + str(f).zfill(3) + " at timestep " + str(t).zfill(2))
		dataDiff = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]
		header1 = hdu1[0].header
		header2 = hdu2[0].header
		wcs1 = WCS(header1, naxis=2)	
		wcs2 = WCS(header2, naxis=2)
	
		UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=-0.5)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=0)
	
		mwa.date = UTCTime1
		sat.compute(mwa)
		xy1 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
		x1 = int(np.floor(xy1[0]))
		y1 = int(np.floor(xy1[1]))

		mwa.date = UTCTime2
		sat.compute(mwa)
		xy2 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
		x2 = int(np.floor(xy2[0]))
		y2 = int(np.floor(xy2[1]))


		dist = int(np.floor(((x1-x2)**2+(y1-y2)**2)**(0.5)))
		size_of_box = int(np.floor((0.3*dist)))
		if size_of_box < 2:
			size_of_box = 2
		displacement = int(np.floor(size_of_box/2))	
		#print("The size of the box is " + str(size_of_box))
		head = Cutout2D(dataDiff, (x2, y2), (size_of_box, size_of_box))
		head_rms = np.sum(head.data)

		tail = Cutout2D(dataDiff, (x1, y1), (size_of_box, size_of_box))
		tail_rms = np.sum(tail.data)


		mwa.date = UTCTime2 + timedelta(seconds=-20)
		sat.compute(mwa)
		xy_rms = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]

		x_rms = int(np.floor(xy_rms[0]))
		y_rms = int(np.floor(xy_rms[1]))

		rms = Cutout2D(dataDiff, (x_rms, y_rms), (1000, 1000))

		rms_rms = np.sqrt(np.mean(rms.data**2))

		snr = (head_rms - tail_rms)/rms_rms
		snr_array[f] = snr/((size_of_box**2)*2)
		numerator_array[f] = (head_rms - tail_rms)/((size_of_box**2)*2)
		denominator_array[f] = rms_rms
	
	i_array = np.linspace(72.335, 103.015, 768)
	plt.subplot(1,3,1)
	plt.plot(i_array, numerator_array)

	plt.subplot(1,3,2)
	plt.plot(i_array, denominator_array)
	
	plt.subplot(1,3,3)
	plt.plot(i_array, snr_array)
	
	plt.show()

