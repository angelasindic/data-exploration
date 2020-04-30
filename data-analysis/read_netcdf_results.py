from netCDF4 import Dataset
import numpy as np
import glob


def read_netCDF(date, variable):
    nc = glob.glob(f'data/l2w/*{date}/*L2W.nc')
    if (len(nc) != 1):
        print(f"no product found for date {date}")
        return None
    filename = nc[0]
    rootgrp = Dataset(filename, 'r')
    return filename, rootgrp.variables[variable][:]


def get_products(date=''):
    nc = glob.glob(f'data/l2w/*{date}*/*L2W.nc')
    if len(nc) == 0:
        print(f"no product found for date {date}")
        return None
    return nc


def aggregate_timeline(date, variable, nlats = 2946, nlons = 2718):
    prod_paths = get_products(date)
    nt = len(prod_paths)
    ts_array = np.empty((nt, nlats, nlons))
    ts_array[:] = np.NaN
    date_array = []

    tidx = 0
    for prod in prod_paths:
        date = get_datestr(prod)
        date_array.append(date)
        rootgrp = Dataset(prod, 'r')
        values = rootgrp.variables[variable][:]
        ts_array[tidx, :, :] = values[0:nlats, 0:nlons]
        rootgrp.close()
        tidx +=1
    return date_array, ts_array


"""also slow"""
def count_nans(all_values):
    return np.apply_along_axis(lambda x: np.count_nonzero(np.isnan(x)), 0, all_values)

#""VERY SLOW, vectorize doesn't help, maybe running twice through the array, count and sum."""
def count_nans_slow(all_values):
    count = lambda x: np.count_nonzero(np.isnan(x).sum(axis=0))
    vcount = np.vectorize(count)
    return vcount(all_values)

def get_datestr(filename): return '-'.join(filename.split('_')[-8:-5])


def scale(X, x_min, x_max):
    nom = (X-X.min(axis=0))*(x_max-x_min)
    denom = X.max(axis=0) - X.min(axis=0)
    denom[denom==0] = 1
    return x_min + nom/denom
