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
from matplotlib.text import OffsetFrom
from numpy import *

waterfall = np.zeros((50,768))
freq_max = np.zeros((768))

hfont = {'fontname':'Helvetica', 'size':15}

for i in range(50):
	for file in glob.glob("2802-" +str(i) + ".txt"):
		lines = loadtxt(file, delimiter=' ', unpack=False)
		length = lines.shape

		print("The length is " + str(length))
		for n in range(length[0]):
			waterfall[i,n] = lines[n]
			print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))

where_are_NAN = isnan(waterfall)
waterfall[where_are_NAN] = 0

for f in range(768):
	freq_max[f] = max(waterfall[:,f])
	print(waterfall[:,f])

waterfall = np.ma.masked_where(waterfall==0, waterfall)
cmap = plt.cm.inferno
cmap.set_bad(color='black')

#fig, axs = plt.subplots(2,1,sharex=True)
#plt.subplots_adjust(hspace=0)


plt.imshow(waterfall, cmap=cmap, interpolation='nearest', aspect='auto', extent=[72.335, 103.015, 0, 49])
plt.colorbar()

#The below are perth transmitters
plt.vlines(92.1, colors='white', ymin=0, ymax=49, linestyles=":")
plt.vlines(92.9, color="white", ymin=0, ymax=49, linestyles=":")
plt.vlines(93.7, colors='white', ymin=0, ymax=49,linestyles=':')
plt.vlines(94.5, colors='white', ymin=0, ymax=49,linestyles=':')
#plt.vlines(95.3, colors='white', ymin=0, ymax=49,linestyles=':')
plt.vlines(96.1, colors='white', ymin=0, ymax=49,linestyles=':')
plt.vlines(96.9, colors='white', ymin=0, ymax=49,linestyles=':')
plt.vlines(97.7, colors='white', ymin=0, ymax=49,linestyles=':')
#plt.vlines(98.5, colors='white', ymin=0, ymax=49,linestyles=':')
plt.vlines(99.3, colors='white', ymin=0, ymax=49,linestyles=':')
plt.vlines(100.1, colors='white', ymin=0, ymax=49,linestyles=':')
plt.vlines(100.9, colors='white', ymin=0, ymax=49,linestyles=':')
#plt.vlines(101.7, colors='white', ymin=0, ymax=49,linestyles=':')
plt.annotate("RTR",xy=(92.2, 40),xycoords='data', rotation=90, color='white')
plt.annotate("PPM",xy=(93, 40),xycoords='data', rotation=90, color='white')
plt.annotate("PER",xy=(93.8, 40),xycoords='data', rotation=90, color='white')
plt.annotate("MIX",xy=(94.6, 40),xycoords='data', rotation=90, color='white')
plt.annotate("NOW",xy=(96.2, 40),xycoords='data', rotation=90, color='white')
plt.annotate("SBSFM",xy=(97, 40),xycoords='data', rotation=90, color='white')
plt.annotate("ABCFM",xy=(97.8, 40),xycoords='data', rotation=90, color='white')
plt.annotate("JJJ",xy=(99.4, 40),xycoords='data', rotation=90, color='white')
plt.annotate("NR",xy=(100.2, 40),xycoords='data', rotation=90, color='white')
plt.annotate("NME",xy=(101, 40),xycoords='data', rotation=90, color='white')




#The below are the transmitters in geraldton
plt.vlines(94.9, colors='yellow', ymin=0, ymax=49,linestyles=':')
#plt.vlines(96.5, colors='yellow', ymin=0, ymax=49,linestyles=':')
plt.vlines(98.1, colors='yellow', ymin=0, ymax=49,linestyles=':')
plt.vlines(98.9, colors='yellow', ymin=0, ymax=49,linestyles=':')
plt.vlines(99.7, colors='yellow', ymin=0, ymax=49,linestyles=':')
plt.vlines(101.3, colors='yellow', ymin=0, ymax=49,linestyles=':')
plt.annotate("ABCFM",xy=(95, 40),xycoords='data', rotation=90, color='yellow')
plt.annotate("BAY",xy=(98.2, 40),xycoords='data', rotation=90, color='yellow')
plt.annotate("JJJ",xy=(99, 40),xycoords='data', rotation=90, color='yellow')
plt.annotate("ABCRN",xy=(99.8, 40),xycoords='data', rotation=90, color='yellow')
plt.annotate("PNN",xy=(101.4, 40),xycoords='data', rotation=90, color='yellow')


#plt.ylim(50, 90)
plt.xlim(85.1, 103.015)

#plt.annotate('', xy=(424, 150),color='orange', rotation = 90,xycoords='figure points')


#plt.annotate('RTR-Perth', xy=(499, 150),color='orange', rotation = 90,xycoords='figure points')

#plt.annotate('PPM-Perth',xy=(538, 150),color='orange', rotation = 90,xycoords='figure points')

#plt.annotate('PER-Perth', xy=(574, 150),color='orange', rotation = 90,xycoords='figure points')


#plt.annotate('MIX-Perth', xy=(613, 150),color='orange', rotation = 90,xycoords='figure points')


#plt.annotate('ABCFM-Geraldton', xy=(633, 150),color='white', rotation = 90,xycoords='figure points')


#plt.annotate('EBA-Perth', xy=(651, 150),color='orange', rotation = 90,xycoords='figure points')

#plt.annotate('NOW-Perth', xy=(689, 150),color='orange', rotation = 90,xycoords='figure points')

#plt.annotate('GGG-Geraldton', xy=(710, 150),color='white', rotation = 90,xycoords='figure points')

#plt.annotate('SBSFM-Perth', xy=(728, 150),color='orange', rotation = 90,xycoords='figure points')


#plt.annotate('ABCFM-Perth', xy=(765, 150),color='orange', rotation = 90,xycoords='figure points')


#plt.annotate('BAY-Geraldton', xy=(785, 150),color='white', rotation = 90,xycoords='figure points')

#plt.annotate('SON-Perth', xy=(805, 150),color='orange', rotation = 90,xycoords='figure points')

#plt.annotate('JJJ-Geraldton', xy=(823, 150),color='white', rotation = 90,xycoords='figure points')

#plt.annotate('JJJ-Perth', xy=(845, 150),color='orange', rotation = 90,xycoords='figure points')


#plt.annotate('ABCRN-Geraldton', xy=(863, 150),color='white', rotation = 90,xycoords='figure points')

#plt.annotate('NR-Perth', xy=(880, 150),color='orange', rotation = 90,xycoords='figure points')

#plt.annotate('NME-Perth', xy=(920, 150),color='orange', rotation = 90,xycoords='figure points')

#plt.annotate('PNN-Geraldton', xy=(936, 150),color='white', rotation = 90,xycoords='figure points')

#plt.annotate('SEN-Perth', xy=(954, 150),color='orange', rotation = 90,xycoords='figure points')


plt.ylabel('Time Steps (s)', **hfont)
plt.xlabel('Frequency (MHz)', **hfont)

#mng = plt.get_current_fig_manager()
#mng.resize(*mng.window.maxsize())
#plt.subplot(2,1,2)
#axs[1].plot(freq_max)

plt.show()
