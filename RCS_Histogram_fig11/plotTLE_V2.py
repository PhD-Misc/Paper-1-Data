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


## note that the original value of pixels is 250

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level
LOS_DISTANCE_ARRAY =[]
RCS_ARRAY = []
SAT_ID_ARRAY = []
TS = 0
a = []
for i in range(58):

    hfont = {'fontname':'Helvetica', 'size':15}
    hdu = fits.open("ALOUETTE-DiffImage" + str(i).zfill(3)+ ".fits")
    data = hdu[0].data
    header = hdu[0].header
    wcs = WCS(hdu[0].header, naxis=2)
    UTCtime = datetime.strptime(header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S') +timedelta(seconds=0)
    mwa.date = UTCtime

    #plt.figure().add_subplot(1,1,1, projection=wcs)
    #plt.imshow(data,  cmap=plt.cm.cubehelix, origin="lower")
    f = open('ALOUETTE_TLE.txt')
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
            if radius < 300 and LOS <= 1000000:
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
                       
                            if float(local_RCS) >= 1:
                                a.append(ID)
                        break
                    rline = q.readline()
        #print('reading line ' +str(counter))
        counter += 1
        line = f.readline()
    print("A total of " + str(satInField) + " are visible in the FOV at " + str(i) )
    TS += satInField



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
            if radius < 300 and LOS <= 1000000:
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
                            if float(local_RCS) >= 1:
                                a.append(ID)
                        break
                    rline = q.readline()
        #print('reading line ' +str(counter))
        counter += 1
        line = f.readline()
    print("A total of " + str(satInField) + " are visible in the FOV at " + str(i) )
    TS += satInField



for i in range(116):

    hfont = {'fontname':'Helvetica', 'size':15}
    hdu = fits.open("ALOS-DiffImage" + str(i).zfill(3)+ ".fits")
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
            if radius < 300 and LOS <= 1000000:
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
                            if float(local_RCS) >= 1:
                                a.append(ID)
                        break
                    rline = q.readline()
        #print('reading line ' +str(counter))
        counter += 1
        line = f.readline()
    print("A total of " + str(satInField) + " are visible in the FOV at " + str(i) )
    TS += satInField


for i in range(116):

    hfont = {'fontname':'Helvetica', 'size':15}
    hdu = fits.open("UKUBE-DiffImage" + str(i).zfill(3)+ ".fits")
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
            if radius < 300 and LOS <= 1000000:
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
                            if float(local_RCS) >= 1:
                                a.append(ID)
                        break
                    rline = q.readline()
        #print('reading line ' +str(counter))
        counter += 1
        line = f.readline()
    print("A total of " + str(satInField) + " are visible in the FOV at " + str(i) )
    TS += satInField

for i in range(116):

    hfont = {'fontname':'Helvetica', 'size':15}
    hdu = fits.open("DUCHIFAT-DiffImage" + str(i).zfill(3)+ ".fits")
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
            if radius < 300 and LOS <= 1000000:
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
                            if float(local_RCS) >= 1:
                                a.append(ID)
                        break
                    rline = q.readline()
        #print('reading line ' +str(counter))
        counter += 1
        line = f.readline()
    print("A total of " + str(satInField) + " are visible in the FOV at " + str(i) )
    TS += satInField



SAT_ID_ARRAY = list(set(SAT_ID_ARRAY))
#print(SAT_ID_ARRAY)
a = list(set(a))
print(a)

r = list(set(RCS_ARRAY))
r = sorted(r, reverse=True) 
#r[:] = [(x/3.14)**(0.5) for x in r]
print(len(r))
TS /= (116*4 + 58)
print("The value of TS is " + str(TS))
#The below is for plotting the RCS histograms
num_bins = 10
hist, bins, patches = plt.hist(r, num_bins)
plt.show()
plt.clf()

logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
plt.hist(r, bins=logbins, facecolor="black", edgecolor="white")
plt.xscale('log')
#plt.ylim(0,15)
plt.xlabel('RCS $(m^{2})$', **hfont)
plt.ylabel("Number of Satellites", **hfont)
plt.grid(axis='y')
plt.show()
plt.clf()

#The below is for plotting the LOS histograms
a = sorted(LOS_DISTANCE_ARRAY, reverse=True)

num_bins = 20
hist, bins, patches = plt.hist(a, num_bins)
plt.show()
plt.clf()
logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
plt.hist(a, bins=logbins, facecolor="black", edgecolor="white")
plt.xscale('log')
plt.grid(axis='y')
plt.show()



