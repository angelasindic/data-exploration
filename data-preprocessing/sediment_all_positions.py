
# process sediment values from all positions from all time, into a big dataframe.
# each column represents a position in satellite image, over time

import os
import glob
import pandas as pd
from netCDF4 import Dataset
import numpy as np

df_temp = pd.DataFrame(columns=['sediment(km2)'])
df = pd.DataFrame()

for folder_name in os.listdir():
    if '-' in folder_name: 
        for file_name in glob.glob(os.getcwd()+ '/' + folder_name + '/*L2W.nc'):
            nc = Dataset(file_name)
            ds = list(nc.variables.keys())
            dataset = ds[3] 
            data_temp = nc.variables[dataset][:]
            data = data_temp.flatten()
            df_temp.loc[1] = [data]
            df_new = pd.DataFrame(df_temp['sediment(km2)'].values.tolist())
            df_new['date'] = folder_name
            df = pd.concat([df, df_new])

df.to_csv('pd_sediment.csv', index=False)      

