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
line1 = "ALOS"
line2 = "1 28931U 06002A   16079.98024251 +.00000391 +00000-0 +86490-4 0  9999"
line3 = "2 28931 097.8961 122.7695 0001002 052.8253 307.3040 14.62149601541084"
sat = ephem.readtle(line1, line2, line3)

#The below section sets the MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level

hfont = {'fontname':'Helvetica', 'size':15}


snr_array = np.zeros((768))
numerator_array = np.zeros((768))
denominator_array = np.zeros((768))
snr_array2 = np.zeros((768))
numerator_array2 = np.zeros((768))
denominator_array2 = np.zeros((768))
for t in range(30):
	t=5
	for f in range(768):
		hdu1 = fits.open("1142340880-2m-" + str(t) + "-" + str(f).zfill(4) + "-image.fits")	
		hdu2 = fits.open("1142340880-2m-" + str(t+1) + "-" + str(f).zfill(4) + "-image.fits")
		print("Working on frequency channel " + str(f).zfill(3) + " at timestep " + str(t).zfill(2))
		dataDiff = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]
		header1 = hdu1[0].header
		header2 = hdu2[0].header
		wcs1 = WCS(header1, naxis=2)	
		wcs2 = WCS(header2, naxis=2)
	
		UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)
	
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
		
		size_of_box=20
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
	
	

	for f in range(768):
		hdu1 = fits.open("1142340880-2m-" + str(t) + "-" + str(f).zfill(4) + "-image.fits")
		hdu2 = fits.open("1142340880-2m-" + str(t+1) + "-" + str(f).zfill(4) + "-image.fits")
		print("Working on frequency channel " + str(f).zfill(3) + " at timestep " + str(t).zfill(2))
		dataDiff = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]
		header1 = hdu1[0].header
		header2 = hdu2[0].header
		wcs1 = WCS(header1, naxis=2)
		wcs2 = WCS(header2, naxis=2)
		
		UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=10)
		UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=15)

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
		size_of_box=20
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
		snr_array2[f] = snr/((size_of_box**2)*2)
		numerator_array2[f] = (head_rms + tail_rms)/((size_of_box**2)*2)
		denominator_array2[f] = rms_rms
		if f == 604:
			head = Cutout2D(dataDiff, (800, 816), (1,1))
			tail = Cutout2D(dataDiff, (720, 832), (1,1))
			head_rms = np.sum(head.data)
			tail_rms = np.sum(tail.data)
			snr = (head_rms - tail_rms)/rms_rms
			snr_array2[f] = snr/((1**2)*2)
			numerator_array2[f] = (head_rms - tail_rms)/((1**2)*2)
			print("The rms is " + str(rms_rms))
			print("Running f 604")
			print("The value of headrms is " + str(head_rms))
			print("The value of tail rms is " + str(tail_rms))
			print("snr is " + str(snr/((1**2)*2)))	
			print("The test value is " + str(snr_array2[f]))	

	
		if f == 645:
                        head = Cutout2D(dataDiff, (800, 760), (1,1))
                        tail = Cutout2D(dataDiff, (970, 740), (1,1))
                        head_rms = np.sum(head.data)
                        tail_rms = np.sum(tail.data)
                        snr = (head_rms - tail_rms)/rms_rms
                        snr_array2[f] = snr/((1**2)*2)
                        numerator_array2[f] = (head_rms - tail_rms)/((1**2)*2)
                        print("The rms is " + str(rms_rms))
                        print("Running f 604")
                        print("The value of headrms is " + str(head_rms))
                        print("The value of tail rms is " + str(tail_rms))
                        print("snr is " + str(snr/((1**2)*2)))
                        print("The test value is " + str(snr_array2[f]))


		if f == 664:
                        head = Cutout2D(dataDiff, (830, 750), (2,2))
                        tail = Cutout2D(dataDiff, (720, 770), (2,2))
                        head_rms = np.sum(head.data)
                        tail_rms = np.sum(tail.data)
                        snr = (head_rms - tail_rms)/rms_rms
                        snr_array2[f] = snr/((2**2)*2)
                        numerator_array2[f] = (head_rms - tail_rms)/((2**2)*2)
                        print("The rms is " + str(rms_rms))
                        print("Running f 604")
                        print("The value of headrms is " + str(head_rms))
                        print("The value of tail rms is " + str(tail_rms))
                        print("snr is " + str(snr/((1**2)*2)))
                        print("The test value is " + str(snr_array2[f]))


	
	i_array = np.linspace(72.335, 103.015, 768)
	num_array = np.linspace(0, 767, 768)
	plt.subplot(2,3,1)
	plt.plot(i_array, numerator_array, color="black")
	plt.xlim(72.335, 103.015)
	plt.grid()
	plt.ylim(-30, 130)	
	plt.text(72.8, 122, 'SIGNAL FROM PATCH OF SKY WITH A SATELLITE', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})

	plt.subplot(2,3,2)
	plt.plot(i_array, denominator_array, color="black")
	plt.xlim(72.335, 103.015)
	plt.grid()
	plt.ylim(0, 65)	
	plt.text(72.8, 62, 'Noise', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})

	plt.subplot(2,3,3)
	plt.plot(i_array, snr_array, color="black")
	plt.ylim(-2, 11)
	plt.xlim(72.335, 103.015)
	plt.grid()
	plt.text(72.8, 10.4, 'DSNRS', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})


	plt.subplot(2,3,4)
        plt.plot(i_array, numerator_array2, color="black")
	plt.xlim(72.335, 103.015)
	plt.grid()
	plt.ylim(-30, 130)	
	plt.text(72.8, 122, 'SIGNAL FROM PATCH OF SKY WITH NO SATELLITE', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})
	plt.xlabel("Frequency (MHz)", **hfont)

        plt.subplot(2,3,5)
        plt.plot(i_array, denominator_array2, color="black")
	plt.xlim(72.335, 103.015)
	plt.grid()
	plt.ylim(0, 65)
	plt.text(72.8, 62, 'Noise', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})
	plt.xlabel("Frequency (MHz)", **hfont)

        plt.subplot(2,3,6)
        plt.plot(i_array, snr_array2, color="black")
	plt.ylim(-2, 11)
	plt.xlim(72.335, 103.015)
	plt.grid()	
	plt.text(72.8, 10.4, 'DSNRS', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})
	plt.xlabel("Frequency (MHz)", **hfont)
	
	plt.annotate('Signal Amplitude (Jy/Beam)',xy=(.09, .7), xycoords='figure fraction',horizontalalignment='left', verticalalignment='top',fontsize=20, rotation=90)
	plt.annotate('Noise RMS (Jy/Beam)',xy=(.37, .655), xycoords='figure fraction',horizontalalignment='left', verticalalignment='top',fontsize=20, rotation=90)
	plt.annotate('DSNRS (Ratio)',xy=(.645, .6), xycoords='figure fraction',horizontalalignment='left', verticalalignment='top',fontsize=20, rotation=90)

	plt.subplots_adjust(hspace=0)	
	plt.show()

