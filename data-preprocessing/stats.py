# calculate the mean, std, and the missing values for each position
# if the percentage of NaN for a location is higher than 80%, then the mean is replaced with NaN, representing land

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sediment_all_positions import read_data

df = read_data(root_dir = os.listdir(), nlats = 2946, nlons = 2718)

def calculate_stats(df):
  """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DateFrame
        the dataframe that contains date as one column and other columns representing sedimentation per location 
    
    Returns
    -------
    df_total : DataFrame
        Columns of the dataframe are mean, std of the sediment values, and missing percentage of NaNs.
        Each row contains values for each location.
    """
  
  df_total = pd.DataFrame() # create an emopty dataframe

  df1 = df.drop(['date'], axis=1)

  # calculate mean, std for each position 
  df_total['mean'] = df1.mean(axis = 0, skipna=True)
  df_total['std'] = df1.std(axis = 0, skipna=True)

  # calculate percentage of missing values
  df_total['missing'] = df1.isnull().sum() * 100 / len(df1) # represents xx percentage of the values are NaNs

  # replace the mean with NaNs, if the percentage of NaNs for the locaton exceeds 80%
  df_total.loc[df_total['missing'] > 80, 'mean'] = float('nan') # if the percentage of NaN higher than 80%, then mean is NaN

  return df_total

#df_total.to_csv('df_mean_std_missing', index = False)
