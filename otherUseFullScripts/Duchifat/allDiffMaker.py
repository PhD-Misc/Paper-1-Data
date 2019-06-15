from astropy.io import fits
import matplotlib.pyplot as plt

for timeStep in range(80):
	for f in range(768):
		hdu1 = fits.open('1142521608-2m-' + str(timeStep) + "-" + str(f).zfill(4) + "-image.fits")
		hdu2 = fits.open('1142521608-2m-' + str(timeStep+1) + "-" + str(f).zfill(4) + "-image.fits")
		print("t=" + str(timeStep) + " of 77 and f=" + str(f))
		data = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]
		plt.imshow(data, origin="lower", cmap=plt.cm.inferno)
		plt.savefig("DiffImage-t" + str(timeStep).zfill(4) + "-f" + str(f).zfill(4) + ".png")
		plt.clf()
