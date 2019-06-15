import astropy
from astropy.io import fits
from astropy.wcs import WCS
import ephem
import numpy as np
import matplotlib.pyplot as plt
import time
from array import *
from numpy import loadtxt
import glob
import os.path


waterfall = np.zeros((78,768))
hfont = {'fontname':'Helvetica', 'size':15}



for i in range(78):
	for file in glob.glob("waterfall-sum-" +str(i) + ".txt"):
		lines = loadtxt(file, delimiter=' ', unpack=False)
		length = lines.shape

		print("The length is " + str(length))
		for n in range(length[0]):
			waterfall[i,n] = lines[n]
			print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))

#this section flags all central freq
r=[16, 48, 80, 112, 144, 176, 208, 240, 272, 304, 336, 368, 400, 432, 464, 496, 528, 560, 592, 624, 656, 688, 720, 752]

for z in r:
        waterfall[:,z]=0


waterfall = np.ma.masked_where(waterfall==0, waterfall)
cmap = plt.cm.inferno
cmap.set_bad(color='black')

plt.imshow(waterfall, cmap=cmap, interpolation='nearest',  aspect='auto', extent=[72.34, 102.97, 77, 1])
#plt.colorbar()
plt.xlabel('Frequency (MHZ)', **hfont)
plt.ylabel('Time Steps (s)', **hfont)
plt.show()
