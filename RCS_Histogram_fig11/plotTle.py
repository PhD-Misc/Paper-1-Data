from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import astropy
from astropy.wcs import WCS
import ephem
from datetime import datetime, timedelta
from array import *
import math
import os.path
from astropy.nddata import Cutout2D


#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level
LOS_DISTANCE_ARRAY =[]
RCS_ARRAY = []
SAT_ID_ARRAY = []
for i in range(116):
    
    hfont = {'fontname':'Helvetica', 'size':15}
    hdu = fits.open("ISS_DiffImage" + str(i).zfill(3)+ ".fits")
    data = hdu[0].data
    header = hdu[0].header
    wcs = WCS(hdu[0].header, naxis=2)
    UTCtime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S') +timedelta(seconds=0)
    mwa.date = UTCtime

    #plt.figure().add_subplot(1,1,1, projection=wcs)
    #plt.imshow(data,  cmap=plt.cm.cubehelix, origin="lower")
    f = open('ISS_TLE.txt')
    line = f.readline()
    counter = 1
    line1 = 'SATELLITE'
    satInField =0
    while line:
        if counter%2 ==1:
            line2 = line
        else:
            line3 = line
            sat=ephem.readtle(str(line1), str(line2),str(line3))
            sat.compute(mwa)
            x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
            radius = ((x-700.0)**2.0 + (y-700.0)**2.0)**(0.5)
            LOS = sat.range
            #if radius < 375 and LOS <= 3000000:
            if radius < 425 and LOS <= 2500000:
                #plt.plot(x,y, 'o', mfc='none', color='yellow', markersize=10)
                ID = int(line[2] + line[3] + line[4] + line[5] + line[6] )
                #print(ID)
                satInField += 1
                print("searching for sat no " +str(ID)) 
                SAT_ID_ARRAY.append(ID)     
                # Magic happens here
                LOS_DISTANCE_ARRAY.append(sat.range/1000.0)
                q = open("RCS.txt")
                rline = q.readline()
                while rline:
                    local_ID =int( rline[13] + rline[14] + rline[15] + rline[16] + rline[17])
                    #print("current ID " + str(local_ID))
                    if ID == local_ID:
                        local_RCS = str(rline[119] + rline[120] + rline[121] + rline[122] + rline[123] + rline[124] + rline[125] + rline[126])
                        local_RCS = local_RCS.replace(" ", "")
                        if local_RCS == "N/A":
                            continue
                        else:
                            RCS_ARRAY.append(float(local_RCS))
                        break
                    rline = q.readline()
        #print('reading line ' +str(counter))
        counter += 1
        line = f.readline()
    print("A total of " + str(satInField) + " are visible in the FOV at " + str(i) )
    #plt.savefig("Image" + str(i).zfill(4) + ".png")
print(set(SAT_ID_ARRAY))
print(set(RCS_ARRAY))
r = list(set(RCS_ARRAY))
r = sorted(r, reverse=True) 
print(len(r))

k = np.linspace(1,len(r), len(r))
num_bins = 8
#plt.subplot(211)
hist, bins, patches = plt.hist(r, num_bins)
plt.show()
plt.clf()

logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
plt.hist(r, bins=logbins)
plt.xscale('log')
plt.show()


#plt.plot(k,r, color="black")
#plt.yscale("log")
#plt.xlim(1, len(r))
#plt.grid(color="black", linestyle="dotted")
#plt.ylabel("RCS", **hfont)
#plt.xlabel("Satellites in FOV Sorted in Descending Order of RCS", **hfont)
#plt.show()

