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


snr = [None]*90
snrf = [None]*90
for timestep in range(90):
	print("working on timestep " +str(timestep))
	data1 = np.zeros((1400,1400))
	data2 = np.zeros((1400,1400))
	freq = [389, 427, 429, 489, 519, 524, 534, 538, 540, 554, 564, 594, 597, 614, 634, 674, 684, 691, 692, 694, 714, 729, 739, 740, 748, 749, 754, 759, 762]
	for f in freq:
		hud1 = fits.open('1142425368-2m-' +str(timestep) + '-' + str(f).zfill(4)+ '-image.fits')
		data = hud1[0].data[0,0,:,:]
		data1+=data;
	for f in freq:
                hud2 = fits.open('1142425368-2m-' +str(timestep+1) + '-' + str(f).zfill(4)+ '-image.fits')
                data = hud2[0].data[0,0,:,:]
                data2+=data;
	length = len(freq)
	dataDiff = data2-data1
	print("The length is " +str(length))
	newData = [ x/length for x in dataDiff]
	
	header1 = hud1[0].header
	header2 = hud2[0].header
	
	wcs1 = WCS(header1, naxis=2)
	wcs2 = WCS(header2, naxis=2)
	
	UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=-0.5)
	UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=0)	

	#The below section calculates the position of the satellite in the top image in the cooridnate system of the top image

	mwa.date = UTCTime1
    	sat.compute(mwa)
    	xy1 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    	x1 = int(np.floor(xy1[0]))
    	y1 = int(np.floor(xy1[1]))


	#The below section calculates the position of the satellite in the top image in the coordinates sytem o fhte top image
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

	head = Cutout2D(dataDiff, (x2,y2), (size_of_box, size_of_box))
    	head_rms = np.sum(head.data)

	tail = Cutout2D(dataDiff, (x1,y1), (size_of_box, size_of_box))

	tail_rms = np.sum(tail.data)
	mwa.date = UTCTime2 + timedelta(seconds=-20)
	sat.compute(mwa)
	xy_rms = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
	x_rms = int(np.floor(xy_rms[0]))
	y_rms = int(np.floor(xy_rms[1]))

	rms = Cutout2D (dataDiff, (x_rms, y_rms), (1000, 1000))
	rms_rms = np.sqrt(np.mean(rms.data**2))
	print("calculating snr")
	
	snr[timestep] = (head_rms-tail_rms)/rms_rms
	
	plt.subplot(2,2,1)
	plt.imshow(dataDiff)

	plt.subplot(2,2,2)
	i_array = np.linspace(0,89, 90)
	plt.plot(i_array, snr,'black')
	
	#The below code is to plot the diff and snr plot for the entire bandwidth
	#hduf1 = fits.open('2sInt-' + str(timestep) + '-image.fits')
	#hduf2 = fits.open('2sInt-' + str(timestep+1) + '-image.fits')

	#dataf1 = hduf1[0].data[0,0,:,:]
	#dataf2 = hduf2[0].data[0,0,:,:]

	#dataDifff = dataf2 - dataf1
	
	

	headf = Cutout2D(dataDifff, (x2,y2), (size_of_box, size_of_box))
	head_rmsf = np.sum(headf.data)
	
	tailf = Cutout2D(dataDifff, (x1,y1), (size_of_box, size_of_box))
	tail_rmsf = np.sum(tailf.data)


	rmsf = Cutout2D(dataDifff, (x_rms, y_rms), (1000,1000))
	rmsf_rms = np.sqrt(np.mean(rmsf.data**2))
	snrf[timestep]= (head_rmsf-tail_rmsf)/rmsf_rms

	plt.subplot(2,2,3)
	plt.imshow(dataDifff)
	
	plt.subplot(2,2,4)
	plt.plot(i_array, snrf, 'black')

	plt.savefig('image' + str(timestep).zfill(4) + '.png')



	
	
