from netCDF4 import Dataset
import numpy as np
import glob


#root dir = 'data/l2w'

def get_products(root_dir, date=''):
    """
    Returns the netCDF4 files containing the results for the given date.

    Parameters
    ----------
    root_dir : starting point to locate result files
        Description of arg1
    date : date str of the format '%Y-%m%-d or parts
        Examples are 2019, 2020-03, 2017-01-31

    Returns
    -------
    str
       Full path to netCDF files for the given date

    """
    nc = glob.glob(f'{root_dir}/*{date}*/*L2W.nc')
    if len(nc) == 0:
        print(f"no product found for date {date}")
        return None
    return nc


def aggregate_timeline(root_dir, date, variable, nlats = 2946, nlons = 2718):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    root_dir : str
        Starting point to locate result files
    date : str
        Date str of the format '%Y-%m%-d or parts. Examples are 2019, 2020-03, 2017-01-31
    variable : str
        Variable name specifying the algorithm used: spm_nechad2016, t_nechad2016, t_dogliotti, fai
    nlats : int
        Dimension of the longitudes, for the default the original value of 2946 is used.
    nlons : int
        Dimension of the latitudes, for the default the original value of 2718 is used.

    Returns
    -------
    (str, array)
        Tuple of dates and values. Dates are a list of date strings with format Y%-m%-%d.
        Values is a 2-dim array containing the result for the given algorithm for each pixel/location,
        dimensions are nlats * nlon

    """
    prod_paths = get_products(root_dir, date)
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
        tidx += 1
    return date_array, ts_array


"""CAUTION sloooooow"""
def count_nans(all_values):
    """
    Counts the number of nan values from the given array along the first/time axis.

    Parameters
    ----------
    arg1 : all_values
        Results for one parameter (spm or turbidity) for all dates

    Returns
    -------
    array
        Aggregate number of nans for each pixel/location per time

    """
    return np.apply_along_axis(lambda x: np.count_nonzero(np.isnan(x)), 0, all_values)


"""VERY SLOW, vectorize doesn't help, maybe running because iterating twice through the array for count and sum."""
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
