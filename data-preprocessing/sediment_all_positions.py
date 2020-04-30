
# process sediment values from all positions from all time, into a big dataframe.
# each column represents a position in satellite image, over time

import os
import glob
import pandas as pd
from netCDF4 import Dataset
import numpy as np

df = pd.DataFrame()
for folder_name in os.listdir():
    if '-' in folder_name: 
        for file_name in glob.glob(os.getcwd()+ '/' + folder_name + '/*L2W.nc'):
            nc = Dataset(file_name)
            ds = list(nc.variables.keys())
            dataset = ds[3] 
            data_temp = nc.variables[dataset][:]
            data = data_temp.flatten('C')
            data_split = np.ma.hsplit(data, 1)
            df_temp = pd.DataFrame(data_split)
            df_temp['date'] = folder_name
            df = pd.concat([df, df_temp])

df.to_csv('pd_all_sediment.csv', index=False) 


