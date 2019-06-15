from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.nddata import Cutout2D
import ephem
from datetime import datetime, timedelta
import time
from astropy.wcs import WCS
#The below section is the TLE date of the satellite
line1 = "ISS"
line2 = "1 25544U 98067A   16078.18872957  .00011987  00000-0  18767-3 0  9997"
line3 = "2 25544  51.6438 151.8661 0001598 315.1341 138.1171 15.54181702990822"
sat = ephem.readtle(line1, line2, line3)

#The below sets MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level

noise_rms = [None]*768
hfont = {'fontname':'Helvetica', 'size': 18}


timeStep=10

for f in range(768):
	hud1 = fits.open('1142425368-2m-' + str(timeStep) + '-' + str(f).zfill(4)+ '-image.fits')	
	hud2 = fits.open('1142425368-2m-' + str(timeStep+1) + '-' + str(f).zfill(4)+ '-image.fits')

	diff = hud2[0].data[0,0,:,:] - hud1[0].data[0,0,:,:]
	header2 = hud2[0].header
	wcs2 = WCS(header2, naxis=2)
	UTCTime2 = datetime.strptime(header2['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=20)

	mwa.date = UTCTime2
	sat.compute(mwa)
	xy1 = wcs2.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]
        x1 = int(np.floor(xy1[0]))
        y1 = int(np.floor(xy1[1]))	

	noise = Cutout2D(diff, (x1, y1), (1000, 1000))
	rms = np.sqrt(np.mean(noise.data**2))
	noise_rms[f] = rms
	print(f)

i_array = np.linspace(72.335, 103.015, 768)
plt.plot(i_array, noise_rms, color='black')
plt.grid()
plt.xlabel("Frequency (MHz)", **hfont)
plt.ylabel("Noise RMS (Jy)", **hfont)
#plt.title(UTCTime2, **hfont)
plt.xlim(72.335, 103.015)
plt.ylim(0,280)
plt.show()

