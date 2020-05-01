
# process sediment values from all positions from all time, into a big dataframe.
# each column represents a position in satellite image, over time

import os
import glob
import pandas as pd
from netCDF4 import Dataset
import numpy as np

root_dir = '/data/results/batch_run'
def read_data(root_dir, variable = 'spm_nechad2016', nlats = 2946, nlons = 2718):
    """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    root_dir : str
        Starting point to locate the folder of the result files, each folder represents the date of satellite image
    variable : str
        Variable name specifying the algorithm used: spm_nechad2016, t_nechad2016, t_dogliotti, fai.
        The default is spm_nechad2016
    nlats : int
        Dimension of the longitudes, for the default the original value of 2946 is used.
    nlons : int
        Dimension of the latitudes, for the default the original value of 2718 is used.
    Returns
    -------
    df : DataFrame
        A dataframe with date and sediment values as columns. Each non-date column represents sediment in a location. 
        Dates are a list of date strings with format Y%-m%-%d.
        Non-date columns contain the result for the given algorithm for each pixel/location,
        dimensions are nlats * nlon
    """
    
    df = pd.DataFrame()
    for folder_name in os.listdir(root_dir):
        product_path = glob.glob(root_dir + '/' + folder_name + '/*L2W.nc')
        if '-' in folder_name: 
            for file_name in product_path:
                nc = Dataset(file_name) 
                data_temp = nc.variables[variable][:]
                data = data_temp.flatten('C') # flatten to a 1D array
                data_split = np.ma.hsplit(data, 1) # split into multiple array
                df_temp = pd.DataFrame(data_split)
                df_temp['date'] = folder_name
                df = pd.concat([df, df_temp])
    return df

#df.to_csv('pd_all_sediment.csv', index=False) 


