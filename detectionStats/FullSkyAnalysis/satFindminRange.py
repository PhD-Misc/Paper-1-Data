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
line2 = "1 25544U 98067A   16078.18872957  .00011987  00000-0  18767-3 0  9997"
line3 = "2 25544  51.6438 151.8661 0001598 315.1341 138.1171 15.54181702990822"
sat = ephem.readtle(line1, line2, line3)

dist = []
for i in range(115):
    hdu = fits.open("ISS_DiffImage" + str(i).zfill(3) + ".fits")
    wcs = WCS(hdu[0].header,naxis=2)
    UTCTime = datetime.strptime(hdu[0].header['DATE-OBS'][:-2], '%Y-%m-%dT%H:%M:%S')
    mwa.date = UTCTime
    sat.compute(mwa)
    dist.append(sat.range)
print(min(dist))
