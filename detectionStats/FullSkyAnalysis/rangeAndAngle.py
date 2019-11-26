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

line1 = "ISS"
line2 = "1 40021U 14033M   16080.72630360  .00001579  00000-0  17313-3 0  9990"
line3 = "2 40021  97.9377 347.0557 0013429   0.3746 359.7479 14.89116495 95096"
sat = ephem.readtle(line1, line2, line3)

dist = []
for i in range(115):
    hdu = fits.open("DUCHIFAT-DiffImage" + str(i).zfill(3) + ".fits")
    wcs = WCS(hdu[0].header,naxis=2)
    UTCTime = datetime.strptime(hdu[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
    mwa.date = UTCTime
    sat.compute(mwa)
    LISRange = sat.range
    x,y = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
    angle = np.sqrt((x-750)**2.0+(y-750)**2.0)*5.0/60.0

    print("The angle is " + str(angle) + " and the distance is " + str(LISRange))
