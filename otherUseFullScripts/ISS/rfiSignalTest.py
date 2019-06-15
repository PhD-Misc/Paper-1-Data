from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

for i in range(30):
	hdu5541 = fits.open('1142425368-2m-' +str(i) +'-0554-image.fits' )
	hdu5542 = fits.open('1142425368-2m-' +str(i+1) +'-0554-image.fits' )
	hdu6641 = fits.open('1142425368-2m-' +str(i) +'-0664-image.fits' )
        hdu6642 = fits.open('1142425368-2m-' +str(i+1) +'-0664-image.fits' )
	print("working on time step " + str(i))
	diff = hdu5542[0].data[0,0,:,:] + hdu6642[0].data[0,0,:,:] - hdu6641[0].data[0,0,:,:] - hdu5541[0].data[0,0,:,:]

	plt.imshow(diff)
	plt.colorbar()
	plt.savefig("rfi" + str(i).zfill(4) + ".png")
	plt.clf()
