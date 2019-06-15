from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from datetime import datetime, timedelta
import ephem
import time
from datetime import datetime, timedelta
import math
import numpy as np

#the below is the TLE of the satellite
line1 = "SAT"
line2 = "1 25288U 98021D   14349.31528324  .00000635  00000-0  21971-3 0  9991"

line3 = "2 25288 086.3976 246.2475 0002242 098.2459 040.7746 14.34226918873885"

sat = ephem.readtle(line1, line2, line3)

#The below section sets the MWA as the observer
mwa = ephem.Observer()
mwa.lon = '116:40:14.93485'
mwa.lat = '-26:42:11.94986'
mwa.elevation = 377.827 #from sea level



time_delay_array = np.linspace(-300, 90, 500)

hfont = {'fontname':'Helvetica', 'size': 15}

i=28
hdu1 = fits.open('1102604896-2m-' +str(i*2) +'-0654-image.fits' )
hdu2 = fits.open('1102604896-2m-' +str(i*2+2) +'-0654-image.fits' )
	
data1 = hdu1[0].data[0,0,:,:]
data2 = hdu2[0].data[0,0,:,:]
print(i)
wcs = WCS(hdu1[0].header, naxis=2)
diff = data2- data1
UTCtime = datetime.strptime(hdu1[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')	

plt.figure().add_subplot(1,1,1, projection=wcs)
plt.imshow(diff,  origin="lower", cmap=plt.cm.inferno)
plt.grid(color='white', ls='dotted')
plt.xlabel("RA (Degrees)", **hfont)
plt.ylabel("DEC (Degrees)", **hfont)
plt.title("UTC " + str(UTCtime),**hfont)
#plt.title("Fine Channel Image", **hfont)
x = []
y =[]
for t in time_delay_array:
	localTime = UTCtime + timedelta(seconds=t)
	mwa.date = localTime
	sat.compute(mwa)
	xy = wcs.all_world2pix([[np.degrees(sat.ra.real), np.degrees(sat.dec.real)]], 1)[0]	
	x.append(int(np.floor(xy[0])))
	y.append(int(np.floor(xy[1])))
	
plt.plot(x,y, '-o', marker=',',linewidth=2,markersize=2, color="black")
plt.colorbar().set_label("Jy/Beam", labelpad=+1, **hfont)
plt.show()	
#plt.savefig('474raw-image' + str(i).zfill(3) + '-.png')
#plt.clf()
