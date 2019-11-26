import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS


hfont = {'fontname':'Helvetica', 'size':15}

for i in range(50):
    i=15
    hdu1 = fits.open("UKUBE-" + str(i) + "-pbcor-I.fits")
    hdu2 = fits.open("UKUBE-" + str(i+1) + "-pbcor-I.fits")

    wcs = WCS(hdu2[0].header, naxis=2)
    date = hdu2[0].header[43]
    dataDiff = hdu2[0].data[0,0,:,:] - hdu1[0].data[0,0,:,:]
    print(i) 
    plt.figure().add_subplot(1,1,1, projection = wcs)
    plt.imshow(dataDiff, cmap=plt.cm.inferno, origin='lower', vmin=-10, vmax=30)
    plt.xlabel('RA (Degrees)', **hfont)
    plt.ylabel('DEC (Degrees)', **hfont)
    plt.colorbar().set_label("Jy/Beam", labelpad=+1, **hfont)
    plt.grid(color='white', linestyle="dotted")
    plt.title("ALOS at UTC " + str(date), **hfont)
    plt.show()
    #plt.savefig("ALOS_Primary_beam_corrected_image.png", bbox_inches="tight")
