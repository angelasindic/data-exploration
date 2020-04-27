import os
import glob
import pandas as pd
from netCDF4 import Dataset

df = pd.DataFrame(columns=['date', 'sediment(km2)'])
df_temp = pd.DataFrame(columns=['date', 'sediment(km2)'])

for folder_name in os.listdir():
    if '-' in folder_name: 
        for file_name in glob.glob(os.getcwd()+ '/' + folder_name + '/*L2W.nc'):
            nc = Dataset(file_name)
            ds = list(nc.variables.keys())
            dataset = ds[3] # spm_nechad2016 represents the sedimentaiton density
            data_temp = nc.variables[dataset][:]
            sediment = data_temp[data_temp>10]
            df_temp.loc[1] = [folder_name] + [len(sediment)*100/1000000]
            df = pd.concat([df, df_temp])
            
df.to_csv('sediment_over_time.csv', index=False)
