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
from numpy import linalg as LA

waterfall = np.zeros((98,768))


for i in range(89):
	for file in glob.glob("waterfall-sum-" +str(i) + ".txt"):
		lines = loadtxt(file, delimiter=' ', unpack=False)
		length = lines.shape

		print("The length is " + str(length))
		for n in range(length[0]):
			waterfall[i,n] = lines[n]
			print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))


waterfall = np.ma.masked_where(waterfall==0, waterfall)
cmap = plt.cm.viridis
cmap.set_bad(color='black')

#plt.imshow(waterfall, cmap=cmap, interpolation='bilinear',  aspect='auto', vmax=800, extent=[72.34, 102.97, 90, 1])
#plt.imshow(waterfall, cmap=cmap, interpolation='bilinear', aspect='auto', vmax=800, extent=[72.335, 103.015, 1, 90])
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

#annotate('MIX-Perth', xy=(613, 150),color='orange', rotation = 90,xycoords='figure points')


#plt.annotate('ABCFM-Geraldton', xy=(633, 150),color='white', rotation = 90,xycoords='figure points')


#plt.annotate('EBA-Perth', xy=(651, 150),color='orange', rotation = 90,xy



rms = np.zeros((768))

for file in glob.glob("rms-15.txt"):
	lines2 = loadtxt(file, delimiter=' ', unpack=False)
	length = lines2.shape
	for n in range(length[0]):
		 rms[n]=50 - lines2[n]
vector = np.linspace(72.335, 103.015, num=768)

print(waterfall.shape)
print(rms.shape)
print(vector.shape)
temp = rms/rms.sum()*1800 
temp[:] += 40


#plt.plot(vector, temp, color='black')

plt.imshow(waterfall, cmap=cmap, interpolation='bilinear', aspect='auto', vmax =800)
plt.imshow( temp)
plt.fill(temp)
plt.show()

