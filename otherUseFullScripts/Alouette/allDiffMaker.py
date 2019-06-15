from astropy.io import fits
import matplotlib.pyplot as plt

for timeStep in range(47):
	
	for f in range(768):
		
		hdu1 = fits.open('1102604896-2m-' + str(timeStep*2) + "-" + str(f).zfill(4) + "-image.fits")
		hdu2 = fits.open('1102604896-2m-' + str(timeStep*2+2) + "-" + str(f).zfill(4) + "-image.fits")
		print("t=" + str(timeStep) + " of 47 and f=" + str(f))
		data = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]
		plt.imshow(data, origin="lower", cmap=plt.cm.inferno)
		plt.savefig("DiffImage-t" + str(timeStep).zfill(4) + "-f" + str(f).zfill(4) + ".png")
		#plt.show()
		plt.clf()
