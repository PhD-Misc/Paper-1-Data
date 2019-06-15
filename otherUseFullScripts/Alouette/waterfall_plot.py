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

waterfall = np.zeros((40,768))
hfont = {'fontname':'Helvetica', 'size':15}


for i in range(40):
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

plt.imshow(waterfall, cmap=cmap, interpolation='nearest',  aspect='auto', extent=[72.34, 102.97, 39, 0], vmax=4)
#plt.imshow(waterfall, cmap=cmap, interpolation='bilinear', aspect='auto')
#plt.colorbar()
#plt.vlines(90.5, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(92.1, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(92.9, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(93.7, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(94.5, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(95.3, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(96.1, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(96.9, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(97.7, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(98.5, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(99.3, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(100.1, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(100.9, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(101.7, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(103.3, colors='orange', ymin=0, ymax=89,linestyles=':')
#plt.vlines(104.9, colors='orange', ymin=0, ymax=89,linestyles=':')

#plt.vlines(94.9, colors='white', ymin=0, ymax=89,linestyles=':')
#plt.vlines(96.5, colors='white', ymin=0, ymax=89,linestyles=':')
#plt.vlines(98.1, colors='white', ymin=0, ymax=89,linestyles=':')
#plt.vlines(98.9, colors='white', ymin=0, ymax=89,linestyles=':')
#plt.vlines(99.7, colors='white', ymin=0, ymax=89,linestyles=':')
#plt.vlines(101.3, colors='white', ymin=0, ymax=89,linestyles=':')
#plt.text(101.3, 10, 'somelabel', va='top', ha='center')

#mng = plt.get_current_fig_manager()
#mng.resize(*mng.window.maxsize())


#plt.ylim(50, 90)
#plt.xlim(85, 103.015)

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

plt.show()
