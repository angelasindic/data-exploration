# calculate the mean, std, and the missing values for each position
# if the percentage of NaN for a location is higher than 80%, then the mean is replaced with NaN, representing land

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from sediment_all_positions import read_data
from add_dates import add_dates

root_dir = '/data/results/batch_run'
#df = read_data(root_dir, variable = 'spm_nechad2016', nlats = 2946, nlons = 2718)
#df_all_dates = add_dates(df)

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

  df1 = df.drop(['DateTime'], axis=1)

  # calculate mean, std for each position 
  df_total['mean'] = df1.mean(axis = 0, skipna=True)
  df_total['std'] = df1.std(axis = 0, skipna=True)

  # calculate percentage of missing values
  df_total['missing'] = df1.isnull().sum() * 100 / len(df1) # represents xx percentage of the values are NaNs

  # replace the mean with NaNs, if the percentage of NaNs for the locaton exceeds 80%
  df_total.loc[df_total['missing'] > 80, 'mean'] = float('nan') # if the percentage of NaN higher than 80%, then mean is NaN
  df_total.loc[df_total['missing'] > 80, 'std'] = float('nan') # if the percentage of NaN higher than 80%, then std is NaN

  return df_total

def add_mean_sediment(df):
    """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DateFrame
        the dataframe that contains date as one column and other columns representing sedimentation per location
    
    Returns
    -------
    df : DataFrame
        a new dataframe with an extra column that represents the mean sedimentation over the AOI for each timestamp
    """
  df['average'] = df.drop('DateTime', axis=1).apply(lambda x: x.mean(), axis=1)
  
  return df
 


def stats_custom(df, start_time = '2019-10', ending_time = '2020-03'):
  """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DateFrame
        the dataframe that contains date as one column and other columns representing sedimentation per location
    
    start_time : str
        the date from which we want to calcuate the mean, std and missing values
        
    end_time : str
        the date until which we want to calcuate the mean, std and missing values
    
    Returns
    -------
    df_total : DataFrame
        Columns of the dataframe are mean, std of the sediment values, and missing percentage of NaNs.
        Each row contains values for each location.
    """
  
  df_total = pd.DataFrame() # create an emopty dataframe
  
  df = df.sort_values(["DateTime"], ascending = (True))
  
  # get the month-year as a separate column
  df['month_year'] = pd.to_datetime(df['DateTime']).dt.to_period('M')
  
  
  idx_start = df[df['month_year']== start_time].index.item() #double check about this
  idx_end = df[df['month_year']== end_time].index.item()
  
  df_select = df[idx_start, idx_end].drop(['DateTime'], axis=1)

  # calculate mean, std for each time period
  
  df_total['mean'] = df_select.mean(axis = 0, skipna=True)
  df_total['std'] = df_select.std(axis = 0, skipna=True)

  # calculate percentage of missing values
  df_total['missing'] = df_select.isnull().sum() * 100 / len(df_select) # represents xx percentage of the values are NaNs

  # replace the mean with NaNs, if the percentage of NaNs for the locaton exceeds 80%
  df_total.loc[df_total['missing'] > 80, 'mean'] = float('nan') # if the percentage of NaN higher than 80%, then mean is NaN
  df_total.loc[df_total['missing'] > 80, 'std'] = float('nan') # if the percentage of NaN higher than 80%, then std is NaN

  return df_total

#df_total.to_csv(root_dir + '/' + 'df_mean_std_missing.csv', index = False)
