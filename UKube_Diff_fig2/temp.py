import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import ephem
import time
from datetime import datetime, timedelta
from array import *
import matplotlib.patches as patches

hfont = {'fontname':'Helvetica', 'size':15}

#The below section is the TLE date of the satellite
line1 = "UKUBE"
line2 = "1 40074U 14037F   16079.81203031  .00001270  00000-0  16363-3 0  9993"
line3 = "2 40074  98.3348 169.0455 0005943  80.4298 279.7595 14.82938013 91827"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level



for i in range(50):
    i=12
    hdu1 = fits.open("UKUBE-" + str(i) + "-pbcor-I.fits")
    hdu2 = fits.open("UKUBE-" + str(i+1) + "-pbcor-I.fits")

    header1 = hdu1[0].header
    header2 = hdu2[0].header

    wcs1 = WCS(header1, naxis=2)
    wcs2 = WCS(header2, naxis=2)

    UTCTime1 = datetime.strptime(header1['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)
    UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=-1.75)
      
    date = hdu2[0].header[43]
    dataDiff = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]

    mwa.date = UTCTime1
    sat.compute(mwa)
    xy1 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x1 = int(np.floor(xy1[0]))
    y1 = int(np.floor(xy1[1]))

    mwa.date = UTCTime2
    sat.compute(mwa)
    xy2 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    x2 = int(np.floor(xy2[0]))
    y2 = int(np.floor(xy2[1]))

    dist = int(np.floor(((x1-x2)**2+(y1-y2)**2)**(0.5)))
    size_of_box = int(np.floor((0.3*dist)))
    if size_of_box < 2:
        size_of_box = 2
    displacement = int(np.floor(size_of_box/2))

    

    ax = plt.subplot(1,1,1, projection=wcs2)
    plt.imshow(dataDiff, cmap=plt.cm.cubehelix, origin='lower', vmax=150, vmin=-80)
    rect_head = patches.Rectangle((x1, y1+13), size_of_box+8, size_of_box+8, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect_head)
    rect_tail = patches.Rectangle((x2-3, y2), size_of_box+8, size_of_box+8, linewidth=1, edgecolor='yellow', facecolor='none')
    ax.add_patch(rect_tail)
    plt.xlabel('RA (Degrees)', **hfont)
    plt.ylabel('DEC (Degrees)', **hfont)
    plt.colorbar().set_label("Jy/Beam", labelpad=+1, **hfont)
    plt.grid(color='white', linestyle="dotted")
    plt.title("UKube-1 at UTC " + str(date), **hfont)
    plt.show()
    
