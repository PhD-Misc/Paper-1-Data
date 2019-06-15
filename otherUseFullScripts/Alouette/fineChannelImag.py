from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
hfont = {'fontname':'Helvetica', 'size': 22}
for i in range(90):
	i+= 35
	hdu1 = fits.open('1102604896-2m-' +str(i*2) +'-0474-image.fits' )
	#hdu2 = fits.open('1102604896-2m-' +str(i*2+2) +'-0474-image.fits' )
	wcs = WCS(hdu1[0].header, naxis=2)
	data1 = hdu1[0].data[0,0,:,:]
	#data2 = hdu2[0].data[0,0,:,:]
	print(i)

	diff =data1
	plt.figure().add_subplot(1,1,1, projection=wcs)
	plt.imshow(diff, cmap=plt.cm.inferno, origin='lower', vmax=150)
	#plt.colorbar()
	plt.grid(color='white', ls='solid')
	plt.xlabel("x pixels (RA)", **hfont)
	plt.ylabel("y pixels (Dec)", **hfont)
	plt.title("Fine Channel Image", **hfont)
	plt.show()
	#plt.clf()
	plt.savefig('474Diff-image' + str(i).zfill(3) + '-.png')
	plt.clf()
