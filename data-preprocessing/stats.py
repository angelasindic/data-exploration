# calculate the mean, std, and the missing values for each position
# if the percentage of NaN for a location is higher than 80%, then the mean is replaced with NaN, representing land

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# calculate mean, std, and missing percentage

df = pd.read_csv('pd_all_sediment.csv')

df1 = df.drop(['date'], axis=1)

df2 = df1.mean(axis = 0, skipna=True)

df3 = df1.std(axis = 0, skipna=True)

df_total = pd.DataFrame()
df_total['mean'] = df2
df_total['std'] = df3

# calculate percentage of missing values

percent_missing = df1.isnull().sum() * 100 / len(df1)
df_total['missing'] = percent_missing

df_total.loc[df_total['missing'] > 80, 'mean'] = float('nan') # if the percentage of NaN higher than 80%, then mean is NaN

df_total.to_csv('df_mean_std_missing', index = False)
