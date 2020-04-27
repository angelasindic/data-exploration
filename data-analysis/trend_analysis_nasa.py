#
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
# import os
#
# import calendar

#algorithm from
#https://podaac.jpl.nasa.gov/forum/viewtopic.php?f=87&t=358

def trend():
    import glob
    from netCDF4 import Dataset

    prod_year = '2019'
    products = glob.glob(f'data/l2w/{prod_year}*/*L2W.nc')

    nlat = 2946
    nlon = 2718

    nt = len(products)
    print(f"number of products used for time analysis: {nt}")
    tur_all = np.empty((nt, int(nlat / 2), int(nlon / 2)))
    print(f"tru_all dim: {tur_all.shape}")

    idx = 0 #idx and nt are the same?!, yep.

    for filename in products:
        ncin = Dataset(filename, 'r')
        tur = ncin.variables['spm_nechad2016'][:]
        print(f"mean: {np.nanmean(tur)}")
        tur_all[idx, :, :] = tur[0:nlat:2, 0:nlon:2]
        ncin.close()
        idx = idx + 1
    print(f"index: {idx}")

    tur = np.empty((idx))
    x = range(idx)
    tur_rate = np.empty((nlat // 2, nlon // 2))

    for i in range(nlon // 2):
        for j in range(nlat // 2):
            tur[:] = tur_all[0:idx, j, i]
            try:
                #Least squares polynomial fit
                z = np.polyfit(x, tur, 1)
                tur_rate[j, i] = z[0] * 3650.0  # for decadel, 365*10
            except:
                #print(f"exception for: {i}, {j}")
                tur_rate[j, i] = 0  # using 'try' and this zero value to try and deal with all the NaNs that were causing the linear regression to fail

    print("finished")
    return tur_rate

