import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
isscsv = pd.read_csv("/media/steve/09e8a6cf-68bf-4e9c-a78b-fdfe6ba02dbf/Paper-1-Data/detectionStats/FullSkyAnalysis/ISSstats.csv")
aloscsv = pd.read_csv("/media/steve/09e8a6cf-68bf-4e9c-a78b-fdfe6ba02dbf/Paper-1-Data/detectionStats/FullSkyAnalysis/ALOSstats.csv")
ukubecsv = pd.read_csv("/media/steve/09e8a6cf-68bf-4e9c-a78b-fdfe6ba02dbf/Paper-1-Data/detectionStats/FullSkyAnalysis/UKUBEstats.csv")
duchifatcsv = pd.read_csv("/media/steve/09e8a6cf-68bf-4e9c-a78b-fdfe6ba02dbf/Paper-1-Data/detectionStats/FullSkyAnalysis/DUCHIFATstats.csv")
alouettecsv = pd.read_csv("/media/steve/09e8a6cf-68bf-4e9c-a78b-fdfe6ba02dbf/Paper-1-Data/detectionStats/FullSkyAnalysis/ALOUETTEstats.csv")
rcs1 = isscsv['RCS']
los1 = isscsv['nearestPass']
rcs2 = aloscsv['RCS']
los2 = aloscsv['nearestPass']
rcs3 = ukubecsv['RCS']
los3 = ukubecsv['nearestPass']
rcs4 = duchifatcsv['RCS']
los4 = duchifatcsv['nearestPass']
rcs5 = alouettecsv['RCS']
los5 = alouettecsv['nearestPass']
for i in range(len(rcs1)):
    plt.plot(rcs1[i],los1[i]/1000.0, marker='x',color='black')
for i in range(len(rcs2)):
    plt.plot(rcs2[i],los2[i]/1000.0, marker='x',color='black')
for i in range(len(rcs3)):
    plt.plot(rcs3[i],los3[i]/1000.0, marker='x',color='black')
for i in range(len(rcs4)):
    plt.plot(rcs4[i],los4[i]/1000.0, marker='x',color='black')
for i in range(len(rcs5)):
    plt.plot(rcs5[i],los5[i]/1000.0, marker='x',color='black')
hfont = {'fontname':'Helvetica', 'size':15}
plt.vlines(1,0,10000)
plt.hlines(1000,0,1000)
temp = np.linspace(0,100, 1000)
plt.fill_between(temp, 0, 1000, facecolor='blue', alpha=0.3, label='Range < 1000 Km')
temp2 = np.linspace(1,100,1000)
plt.fill_between(temp2,10000,0, facecolors='red', alpha=0.3,label='RCS > 1.0 $(m^{2})$')



plt.xlabel("RCS $(m^{2})$",**hfont)
plt.ylabel("Shortest Range During Pass (Km)",**hfont)
plt.xscale('log')
plt.yscale('log')

Ukube_range = 642.729875
ALOS_range = 712.8643125
DUCHIFAT_range = 623.325625
ALOUETTE_range = 2184.95025
ISS_range = 437.41359375

UKube_RCS = 0.1180
ALOS_RCS = 13.5930
DUCHIFAT_RCS = 0.0370
ALOUETTE_RCS = 0.9848
ISS_RCS = 399.0524

sat1 = plt.plot(UKube_RCS,Ukube_range, marker='^',color='yellow',markeredgecolor='black',markersize=10, label='UKube-1')
sat2 = plt.plot(DUCHIFAT_RCS,DUCHIFAT_range, marker='<',color='yellow',markeredgecolor='black',markersize=10, label='Duchifat-1')
sat3 = plt.plot(ALOS_RCS,ALOS_range, marker='o',color='lime',markeredgecolor='black',markersize=10,label = 'ALOS')
sat4 = plt.plot(ALOUETTE_RCS,ALOUETTE_range, marker='s',color='lime',markeredgecolor='black',markersize=10, label='Alouette-2')
#plt.plot(ISS_RCS,ISS_range, marker='o',color='lime',markeredgecolor='black',markersize=10)
plt.legend()
plt.show()
