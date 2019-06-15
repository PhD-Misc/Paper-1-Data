from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.wcs import WCS
import ephem
import time
from datetime import datetime, timedelta
from array import *
import os.path
from astropy.nddata import Cutout2D
import math


#the below is the TLE of the satellite
line1 = "SAT"
line2 = "1 25288U 98021D   14349.31528324  .00000635  00000-0  21971-3 0  9991"

line3 = "2 25288 086.3976 246.2475 0002242 098.2459 040.7746 14.34226918873885"

sat = ephem.readtle(line1, line2, line3)

#The below section sets the MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level

for m in range(116):
    m += 25
    array = np.zeros(500)
    time_delay_array = np.linspace(-30, 90, 500)
    #print(time_delay_array)

    kernal = np.zeros(25)
    temp_array = np.zeros(500)

    #The below is for obtaining the gain factor of the psf
    hdu_psf = fits.open("fullskyImage-psf.fits")
    psf = hdu_psf[0].data[0,0,:,:]
    kernal = Cutout2D(psf, position=[700,700], size=[50,50])
    gain_factor = np.reshape(kernal.data, (2500))
    gain = np.ones((10,10))


    for i in range(7):
	hdu = fits.open("ALOUETTE-DiffImage" + str(i+m).zfill(3) + ".fits")
	data = hdu[0].data
	image_rms = np.sqrt(np.mean(data**2))
	UTCTime = datetime.strptime(hdu[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
	wcs = WCS(hdu[0].header, naxis=2)
	counter=0
	for t in time_delay_array:
		localTime = UTCTime + timedelta(seconds=t)
		mwa.date = localTime
		sat.compute(mwa)
		xy = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
		x = int(np.floor(xy[0]))
		y = int(np.floor(xy[1]))
		local_area = Cutout2D(data, position=[x,y], size=[50,50])
		local_area.data = local_area.data - local_area.data.mean()
		local_area.data = local_area.data/ local_area.data.max()
		temp = np.sum(local_area.data*kernal.data)
		temp_array[counter] = temp/625
		array[counter] += temp/625
		counter += 1
	plt.subplot(2,1,1)
	plt.plot(time_delay_array, array)
	plt.title("The value of i is " + str(i)+ " and the value of m is "+str(m) )
	plt.subplot(2,1,2)
	plt.plot(time_delay_array, temp_array)
	plt.title("The value of i is " + str(i) + " and the value of m is " + str(m)  )
	plt.grid(color="black", linestyle='dotted')
        #plt.show(block=False)
	
        if i == 6:
            plt.show()
            #plt.savefig("StackedImage" + str(m).zfill(4) + "ns" + str(7)  +".png")
            print("Saving the stacked image at i value " + str(i) + " and the value of m is " + str(m))
        plt.clf()


