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

timestep=73
snr = [None]*768
position = (534,146)
size = (5,5)
hfont = {'fontname':'Helvetica', 'size':15}

for f in range(768):
	hdu1 = fits.open('1142425368-2m-' +str(timestep) + '-' + str(f).zfill(4)+ '-image.fits')
	hdu2 = fits.open('1142425368-2m-' +str(timestep+1) + '-' + str(f).zfill(4)+ '-image.fits')
	
	diff = hdu2[0].data[0,0,:,:]

	cutout = Cutout2D(diff, position, size)
	print("working on freq channel " + str(f))
	signal = np.sum(cutout.data)
	rms = np.sqrt(np.mean(diff**2))	
	snr[f] = signal/(rms*50)

#freq_array = np.linspace(87.91, 102.97, 768)
freq_array = np.linspace(72.335,103.015, 768)
plt.plot(freq_array, snr, color="black")
plt.grid()
plt.xlim(72.335, 103.015)
plt.ylabel("DSNRS", **hfont)
plt.xlabel("Frequency", **hfont)
plt.show()

