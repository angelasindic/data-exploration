########## to be cleaned up #########

import os
import glob
import pandas as pd
from netCDF4 import Dataset

df = pd.DataFrame()
name_list = []
for folder_name in os.listdir():
    name_list.append(folder_name)
    df['date'] = name_list
    for file_name in glob.glob(os.getcwd()+ '/' + folder_name + '/*L2W.nc'):
        nc = Dataset(file_name)
        ds = list(nc.variables.keys())
        dataset = ds[3] # spm_nechad2016 represents the sedimentaiton density
        data_temp = nc.variables[dataset][:]
        sediment = data_temp[data_temp>10]
        df['sediment (km2)'] = len(sediment) * 100 / 1000000 
        
df.to_csv('sediment_over_time.csv', index=False)
