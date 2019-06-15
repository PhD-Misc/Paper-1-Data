from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from datetime import datetime, timedelta

hfont = {'fontname':'Helvetica', 'size': 15}
for i in range(90):
	hdu1 = fits.open('1142425368-2m-' +str(i) +'-0614-image.fits' )
	hdu2 = fits.open('1142425368-2m-' +str(i+1) +'-0614-image.fits' )
	wcs = WCS(hdu2[0].header, naxis=2)
	data1 = hdu1[0].data[0,0,:,:]
	data2 = hdu2[0].data[0,0,:,:]
	print(i)
	UTCtime = datetime.strptime(hdu2[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
	diff =data2
	plt.figure().add_subplot(1,1,1, projection=wcs)
	plt.imshow(diff, cmap=plt.cm.cubehelix, origin='lower', vmin=-50)
	plt.grid(color='white', ls='dotted')
	plt.xlabel("RA (Degrees)", **hfont)
	plt.ylabel("DEC (Degrees)", **hfont)
	#plt.title("Channel With Direct FM Reception", **hfont)
	plt.colorbar().set_label("Jy/Beam", labelpad=+1, **hfont)
	plt.title("UTC " + str(UTCtime), **hfont)
	plt.show()
	plt.clf()
	#plt.savefig('554Diff-image' + str(i).zfill(3) + '-.png')

