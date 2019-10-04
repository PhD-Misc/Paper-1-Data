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
import csv

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level

threshold = 230
dist = 5000000.0
with open('ALOUETTEstats.csv','w') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['id','RCS','nearestPass'])
    
    SAT_ID_ARRAY = []
    checkedSats = []
    for i in range(58):
        hdu = fits.open("ALOUETTE-DiffImage" + str(i).zfill(3) + ".fits")
        wcs = WCS(hdu[0].header,naxis=2)
        UTCTime = datetime.strptime(hdu[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
        mwa.date = UTCTime
        q = open("ALOUETTEFULL.txt")
        line = q.readline()
        counter = 1
        checkedSats = []
        line1 = 'sat'
        while line:
            print(counter)
            if counter%2 == 1:
                line2 = line
            else:
                line3 = line
                ID = int(line[2] + line[3] + line[4] + line[5] + line[6])
                if ID  in checkedSats or ID in SAT_ID_ARRAY:
                    counter += 1
                    line = q.readline()
                    continue
                else:
                    checkedSats.append(ID)

                sat = ephem.readtle(str(line1),str(line2),str(line3))
                mwa.date = UTCTime
                sat.compute(mwa)
                x, y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
                radius = ((x-700.0)**2.0 + (y-700.0)**2.0)**(0.5)
                if radius <= threshold and sat.range < dist:
                    ID = int(line[2] + line[3] + line[4] + line[5] + line[6] )
                    SAT_ID_ARRAY.append(ID)
                    w = open("RCS.txt")
                    rline = w.readline()
                    while rline:
                        local_ID =int( rline[13] + rline[14] + rline[15] + rline[16] + rline[17])
                        if ID == local_ID:
                            local_RCS = str(rline[119] + rline[120] + rline[121] + rline[122] + rline[123] + rline[124] + rline[125] + rline[126])
                            local_RCS = local_RCS.replace(" ", "")
                        rline = w.readline()
                    los = []
                    for k in range(58):
                        hdu2 = fits.open("ALOUETTE-DiffImage" + str(k).zfill(3) + ".fits")
                        wcs2 = WCS(hdu2[0].header,naxis=2)
                        UTCTime2 = datetime.strptime(hdu2[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
                        mwa.date = UTCTime2
                        sat.compute(mwa)
                        los.append(sat.range)
                    output = [ID,local_RCS,min(los)]
                    thewriter.writerow(output)

            counter += 1
            line = q.readline()
