from astropy.wcs import WCS
import ephem
import time
from astropy.io import fits
from datetime import datetime, timedelta
from array import *
import os.path
import math
from astropy.nddata import Cutout2D
import numpy as np

fineChannels = [423, 425, 426, 427, 428, 429, 433, 436, 438, 449, 453, 458, 472, 473, 474, 481, 486, 487, 488, 489, 493, 496, 506, 507, 508, 513, 514, 517, 518, 519, 523, 528, 532, 533, 534, 537, 538, 539, 552, 553, 554, 561, 563, 564, 578, 593, 594, 595, 596, 598, 602, 603, 604, 613, 621, 633, 634, 642, 644, 653, 658, 664, 665, 666, 673, 674, 683, 685, 686, 690, 691, 692, 693, 708, 713, 715, 716, 723, 724, 728, 729, 738, 739, 740, 741, 742, 743, 744, 747, 748, 749, 753, 757, 758, 759, 760, 761, 763]



for timeStep in range(77):
	data1 = np.zeros((1400, 1400))
	data2 = np.zeros((1400, 1400))
	for f in fineChannels:
		hdu1 = fits.open("1142425368-2m-" + str(timeStep) + "-" + str(f).zfill(4) + "-image.fits" )
		hdu2 = fits.open("1142425368-2m-" + str(timeStep+1) + "-" + str(f).zfill(4) + "-image.fits" )
		data1+= hdu1[0].data[0,0,:,:]
		data2+= hdu2[0].data[0,0,:,:]
		data1[:] = [x1/2.0 for x1 in data1]
		data2[:] = [x2/2.0 for x2 in data2]
	diff = data2 - data1
	header = hdu2[0].header
	print("Making Difference image " + str(timeStep) + " of 77")
	hdu = fits.PrimaryHDU(diff, header=header)
	hdu.writeto("DiffImage_FineChannelsCombined" + str(timeStep).zfill(3) + ".fits")
	
