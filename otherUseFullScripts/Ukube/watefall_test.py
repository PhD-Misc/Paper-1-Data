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
line2 = "1 25510U 98061C   16078.54735601  .00000349  00000-0  51252-4 0  9995"
line3 = "2 25510  31.4341 233.1475 0329000   1.0295  72.1197 14.36970998911720"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level


waterfall=np.zeros((90, 768))

for timeStep in range(90):
	print("working on timestep " +str(timeStep))
	for f in range(768):
		print("Frequency channel " + str(f))
		hud1 = fits.open('1142351440-2m-' + str(timeStep) + '-' + str(f).zfill(4)+ '-image.fits')
		hud2 = fits.open('1142351440-2m-' + str(timeStep+1) + '-' + str(f).zfill(4)+ '-image.fits')

		header1 = hud1[0].header
		header2 = hud2[0].header
		
		wcs1 = WCS(header1, naxis=2)
		wcs2 = WCS(header2, naxis=2)

		#UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=-1)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=-1)
		

		#The below section calculates the position of the satellite in the top image in the cooridnate system of the top image

		#mwa.date = UTCTime1
		#sat.compute(mwa)
    		#xy1 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    		#x1 = int(np.floor(xy1[0]))
    		#y1 = int(np.floor(xy1[1]))


		#The below section calculates the position of the satellite in the top image in the coordinates sytem o fhte top image
		mwa.date = UTCTime2
		sat.compute(mwa)
		xy2 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
		x2 = int(np.floor(xy2[0]))
		y2 = int(np.floor(xy2[1]))

		#print("making diff images")
		#The below section calculates the diff image 2D array
		data1 = np.array(hud1[0].data[0,0,:,:])
		data2 = np.array(hud2[0].data[0,0,:,:])
		dataDiff = data2 - data1


		#The below calculates the snumber of pixels between the head and the tail positions
		#dist = int(np.floor(((x1-x2)**2+(y1-y2)**2)**(0.5)))
		#size_of_box = int(np.floor((0.3*dist)))
		#if size_of_box < 2:
		#	size_of_box = 2
		#displacement = int(np.floor(size_of_box/2))
		size_of_box = 10

		#The below code isolates the head and the tail patches of hte streak
		head = Cutout2D(dataDiff, (x2,y2), (size_of_box, size_of_box))
		head_rms = np.sum(head.data)
		
		#tail = Cutout2D(dataDiff, (x1,y1), (size_of_box, size_of_box))
		#tail_rms = np.sum(tail.data)

		#The below code isolates the box used to calculate the rms
		mwa.date = UTCTime2 + timedelta(seconds=-20)
		sat.compute(mwa)
		xy_rms = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
		x_rms = int(np.floor(xy_rms[0]))
		y_rms = int(np.floor(xy_rms[1]))

		rms = Cutout2D (dataDiff, (x_rms, y_rms), (1000, 1000))

		rms_rms = np.sqrt(np.mean(rms.data**2))

		snr=(head_rms)/rms_rms
		waterfall[timeStep, f] = snr/((size_of_box**2))
		
		np.savetxt("25510-m1-" + str(timeStep) + ".txt", waterfall[timeStep,:])

plt.imshow(waterfall, cmap=plt.cm.viridis, interpolation='bilinear', aspect='auto')
plt.colorbar()
plt.show()



