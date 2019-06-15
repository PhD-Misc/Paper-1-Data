from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
hfont = {'fontname':'Helvetica', 'size': 15}
for i in range(90):
	i=5
	hdu1 = fits.open('1142340880-2m-' +str(i) +'-0664-image.fits' )
	hdu2 = fits.open('1142340880-2m-' +str(i+1) +'-0664-image.fits' )
	wcs = WCS(hdu2[0].header, naxis=2)
	data1 = hdu1[0].data[0,0,:,:]
	data2 = hdu2[0].data[0,0,:,:]
	print(i)

	diff =data2 - data1
	plt.figure().add_subplot(1,1,1)
	plt.imshow(diff, cmap=plt.cm.cubehelix, origin='lower')
	plt.grid(color='white', ls='dotted')
	plt.xlabel("RA (Degrees)", **hfont)
	plt.ylabel("DEC (Degrees)", **hfont)
	plt.title("Channel With Direct FM Reception", **hfont)
	plt.colorbar()
	plt.show()
	plt.clf()
	#plt.savefig('554Diff-image' + str(i).zfill(3) + '-.png')

