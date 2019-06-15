from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from datetime import datetime, timedelta


hfont = {'fontname':'Helvetica', 'size': 15}
for i in range(90):
	hdu1 = fits.open('1102604896-2m-' +str(i*2) +'-0474-image.fits' )
	#hdu2 = fits.open('1142425368-2m-' +str(i+1) +'-0691-image.fits' )
	
	data1 = hdu1[0].data[0,0,:,:]
	#data2 = hdu2[0].data[0,0,:,:]
	print(i)
	wcs = WCS(hdu1[0].header, naxis=2)
	diff = data1
	UTCtime = datetime.strptime(hdu1[0].header['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')	

	plt.figure().add_subplot(1,1,1, projection=wcs)
	plt.imshow(diff, vmax=100, origin="lower", cmap=plt.cm.cubehelix)
	plt.grid(color='white', ls='dotted')
	plt.xlabel("RA (Degrees)", **hfont)
	plt.ylabel("DEC (Degrees)", **hfont)
	plt.title("UTC " + str(UTCtime),**hfont)
	#plt.title("Fine Channel Image", **hfont)
	plt.colorbar().set_label("Jy/Beam", labelpad=+1, **hfont)
	plt.show()	
	#plt.savefig('474raw-image' + str(i).zfill(3) + '-.png')
	#plt.clf()
