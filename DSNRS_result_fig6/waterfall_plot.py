from astropy.io import fits
from astropy.wcs import WCS
import ephem
import numpy as np
import matplotlib.pyplot as plt
import time
from  array import *
from numpy import loadtxt
import glob
import os.path
from matplotlib.text import OffsetFrom
from numpy import *

hfont = {'fontname':'Helvetica', 'size':18}
waterfallISS = np.zeros((49, 768))
waterfallALOS = np.zeros((40, 768))
waterfallALOUETTE = np.zeros((46, 768))
waterfallUKUBE = np.zeros((60, 768))
waterfallDUCHIFAT = np.zeros((69, 768))
	
for i in range(49):
	for file in glob.glob("ISS_waterfall-sum-" + str(i) + ".txt"):
		lines = loadtxt(file, delimiter=" ", unpack=False)
		length = lines.shape

		print("The length is " + str(length))
		for n in range(length[0]):
			waterfallISS[i,n] = lines[n]
			print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))


for i in range(40):
        for file in glob.glob("ALOS_waterfall-sum-" + str(i) + ".txt"):
                lines = loadtxt(file, delimiter=" ", unpack=False)
                length = lines.shape

                print("The length is " + str(length))
                for n in range(length[0]):
                        waterfallALOS[i,n] = lines[n]
                        print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))


for i in range(46):
        for file in glob.glob("ALOUETTE_waterfall-sum-" + str(i) + ".txt"):
                lines = loadtxt(file, delimiter=" ", unpack=False)
                length = lines.shape

                print("The length is " + str(length))
                for n in range(length[0]):
                        waterfallALOUETTE[i,n] = lines[n]
                        print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))


for i in range(69):
        for file in glob.glob("DUCHIFAT_waterfall-sum-" + str(i) + ".txt"):
                lines = loadtxt(file, delimiter=" ", unpack=False)
                length = lines.shape

                print("The length is " + str(length))
                for n in range(length[0]):
                        waterfallDUCHIFAT[i,n] = lines[n]
                        print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))


for i in range(60):
        for file in glob.glob("UKUBE_waterfall-sum-" + str(i) + ".txt"):
                lines = loadtxt(file, delimiter=" ", unpack=False)
                length = lines.shape

                print("The length is " + str(length))
                for n in range(length[0]):
                        waterfallUKUBE[i,n] = lines[n]
                        print("Extracting channel " + str(n) + " and the value is " + str(lines[n]))


r=[16, 48, 80, 112, 144, 176, 208, 240, 272, 304, 336, 368, 400, 432, 464, 496, 528, 560, 592, 624, 656, 688, 720, 752]

for z in r:
        waterfallALOUETTE[:,z]=0
	waterfallUKUBE[:,z]=0
	waterfallDUCHIFAT[:,z]=0
	



waterfallISS = np.ma.masked_where(waterfallISS==0, waterfallISS)
cmap = plt.cm.cubehelix
cmap.set_bad(color='black')


waterfallALOS = np.ma.masked_where(waterfallALOS==0, waterfallALOS)
cmap = plt.cm.cubehelix
cmap.set_bad(color='black')



waterfallALOUETTE = np.ma.masked_where(waterfallALOUETTE==0, waterfallALOUETTE)
cmap = plt.cm.cubehelix
cmap.set_bad(color='black')



waterfallUKUBE = np.ma.masked_where(waterfallUKUBE==0, waterfallUKUBE)
cmap = plt.cm.cubehelix
cmap.set_bad(color='black')



waterfallDUCHIFAT = np.ma.masked_where(waterfallDUCHIFAT==0, waterfallDUCHIFAT)
cmap = plt.cm.cubehelix
cmap.set_bad(color='black')




fig = plt.figure()
ax1 = plt.subplot(511)
ax2 = plt.subplot(512)
ax3 = plt.subplot(513)
ax4 = plt.subplot(514)
ax5 = plt.subplot(515)


a1=ax1.imshow(waterfallISS, origin="upper", interpolation="nearest",cmap=cmap, aspect="auto", extent=[72.335, 103.015, 48, 0], vmin=-2, vmax=8)
ax1.text(75, 6, 'ISS', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})
a2=ax2.imshow(waterfallALOS, origin="upper", interpolation="nearest",cmap=cmap ,aspect="auto", extent=[72.335, 103.015, 39, 0], vmin=-2, vmax=8)
ax2.text(75, 5, 'ALOS', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})
a3=ax3.imshow(waterfallALOUETTE, origin="upper", interpolation="nearest",cmap=cmap, aspect="auto", extent=[72.335, 103.015, 91, 0], vmin=-2,vmax=8)
ax3.text(75, 11, 'Alouette-2', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})
a4=ax4.imshow(waterfallUKUBE, origin="upper", interpolation="nearest",cmap=cmap ,aspect="auto", extent=[72.335, 103.015, 59, 0], vmin=-2, vmax=8)
ax4.text(75, 7, 'UKube-1', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})
a5=ax5.imshow(waterfallDUCHIFAT, origin="upper", interpolation="nearest",cmap=cmap, aspect="auto", extent=[72.335, 103.015, 68, 0], vmin=-2, vmax=8)
ax5.text(75, 8, 'Duchifat-1', fontsize=10,bbox={'facecolor':'white', 'alpha':1, 'pad':5})


#FM stations for ISS
#The below are perth transmitters
ax1.vlines(92.1, colors='white', ymin=0, ymax=48, linestyles=":", linewidth=1)
ax1.vlines(92.9, color="white", ymin=0, ymax=48, linestyles=":", linewidth=1)
ax1.vlines(93.7, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(94.5, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
#plt.vlines(95.3, colors='white', ymin=0, ymax=49,linestyles=':')
ax1.vlines(96.1, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(96.9, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(97.7, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
#plt.vlines(98.5, colors='white', ymin=0, ymax=49,linestyles=':')
ax1.vlines(99.3, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(100.1, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(100.9, colors='white', ymin=0, ymax=48,linestyles=':', linewidth=1)
#plt.vlines(101.7, colors='white', ymin=0, ymax=49,linestyles=':')
#ax1.annotate("RTR",xy=(92.2, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("PPM",xy=(93, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("PER",xy=(93.8, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("MIX",xy=(94.6, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("NOW",xy=(96.2, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("SBSFM",xy=(97, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("ABCFM",xy=(97.8, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("JJJ",xy=(99.4, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("NR",xy=(100.2, 35),xycoords='data', rotation=90, color='white')
#ax1.annotate("NME",xy=(101, 35),xycoords='data', rotation=90, color='white')

#The below are the transmitters in geraldton
ax1.vlines(94.9, colors='yellow', ymin=0, ymax=48,linestyles=':', linewidth=1)
#plt.vlines(96.5, colors='yellow', ymin=0, ymax=49,linestyles=':')
ax1.vlines(98.1, colors='yellow', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(98.9, colors='yellow', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(99.7, colors='yellow', ymin=0, ymax=48,linestyles=':', linewidth=1)
ax1.vlines(101.3, colors='yellow', ymin=0, ymax=48,linestyles=':', linewidth=1)
#ax1.annotate("ABCFM",xy=(95, 35),xycoords='data', rotation=90, color='yellow')
#ax1.annotate("BAY",xy=(98.2, 35),xycoords='data', rotation=90, color='yellow')
#ax1.annotate("JJJ",xy=(99, 35),xycoords='data', rotation=90, color='yellow')
#ax1.annotate("ABCRN",xy=(99.8, 35),xycoords='data', rotation=90, color='yellow')
#ax1.annotate("PNN",xy=(101.4, 35),xycoords='data', rotation=90, color='yellow')




#The below are the FM stations for ALOS
#The below are perth transmitters
ax2.vlines(92.1, colors='white', ymin=0, ymax=39, linestyles=":", linewidth=1)
ax2.vlines(92.9, color="white", ymin=0, ymax=39, linestyles=":", linewidth=1)
#plt.vlines(93.7, colors='white', ymin=0, ymax=34,linestyles=':')
ax2.vlines(94.5, colors='white', ymin=0, ymax=39,linestyles=':', linewidth=1)
#plt.vlines(95.3, colors='white', ymin=0, ymax=49,linestyles=':')
ax2.vlines(96.1, colors='white', ymin=0, ymax=39,linestyles=':', linewidth=1)
ax2.vlines(96.9, colors='white', ymin=0, ymax=39,linestyles=':', linewidth=1)
ax2.vlines(97.7, colors='white', ymin=0, ymax=39,linestyles=':', linewidth=1)
#plt.vlines(98.5, colors='white', ymin=0, ymax=49,linestyles=':')
ax2.vlines(99.3, colors='white', ymin=0, ymax=39,linestyles=':',linewidth=1)
#plt.vlines(100.1, colors='white', ymin=0, ymax=34,linestyles=':')
#plt.vlines(100.9, colors='white', ymin=0, ymax=34,linestyles=':')
#plt.vlines(101.7, colors='white', ymin=0, ymax=49,linestyles=':')
#ax2.annotate("RTR",xy=(92.2, 25),xycoords='data', rotation=90, color='white')
#ax2.annotate("PPM",xy=(93, 25),xycoords='data', rotation=90, color='white')
#plt.annotate("PER",xy=(93.8, 25),xycoords='data', rotation=90, color='white')
#ax2.annotate("MIX",xy=(94.6, 25),xycoords='data', rotation=90, color='white')
#ax2.annotate("NOW",xy=(96.2, 25),xycoords='data', rotation=90, color='white')
#ax2.annotate("SBSFM",xy=(97, 25),xycoords='data', rotation=90, color='white')
#ax2.annotate("ABCFM",xy=(97.8, 25),xycoords='data', rotation=90, color='white')
#ax2.annotate("JJJ",xy=(99.4, 25),xycoords='data', rotation=90, color='white')
#The below are the transmitters in geraldton
ax2.vlines(94.9, colors='yellow', ymin=0, ymax=39,linestyles=':', linewidth=1)
#plt.vlines(96.5, colors='yellow', ymin=0, ymax=49,linestyles=':')
#plt.vlines(98.1, colors='yellow', ymin=0, ymax=34,linestyles=':')
#plt.vlines(98.9, colors='yellow', ymin=0, ymax=34,linestyles=':')
#plt.vlines(99.7, colors='yellow', ymin=0, ymax=34,linestyles=':')
ax2.vlines(101.3, colors='yellow', ymin=0, ymax=39,linestyles=':', linewidth=1)
#ax2.annotate("ABCFM",xy=(95, 25),xycoords='data', rotation=90, color='yellow')
#plt.annotate("BAY",xy=(98.2, 25),xycoords='data', rotation=90, color='yellow')
#plt.annotate("JJJ",xy=(99, 25),xycoords='data', rotation=90, color='yellow')
#plt.annotate("ABCRN",xy=(99.8, 25),xycoords='data', rotation=90, color='yellow')
#ax2.annotate("PNN",xy=(101.4, 25),xycoords='data', rotation=90, color='yellow')

#ax1.set_title("Dynamic SNR Spectrum (DSNRS) Plots", **hfont)
#ax2.set_ylabel("ALOS", **hfont)
ax3.set_ylabel("Time Since Start of Observation (s)", **hfont)
#ax4.set_ylabel("UKube 1", **hfont)
#ax5.set_ylabel("Duchifat 1", **hfont)
#plt.ylabel("Timesteps (s)", **hfont)
plt.subplots_adjust(hspace=0)
plt.xlabel("Frequency (MHz)", **hfont)

#plt.colorbar(a1, ax=ax1)
#plt.colorbar(a2, ax=ax2)
#plt.colorbar(a3, ax=ax3)
#plt.colorbar(a4, ax=ax4)
#plt.colorbar(a5, ax=ax5)
customax = fig.add_axes([0.91, 0.11, 0.015, 0.77])
plt.colorbar(a4, orientation='vertical',  cax=customax).set_label("DSNRS (Ratio)",labelpad=-0.5,**hfont)
plt.show()










