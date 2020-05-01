# the sediment time series for different positions are plotted together for comparison

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sediment_all_positions import read_data

root_dir = '/data/results/batch_run'
#df = read_data(root_dir, variable = 'spm_nechad2016', nlats = 2946, nlons = 2718)

def restrain_area(df, threshold_water = 5, threshold_land = 80):
  """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DateFrame
        the dataframe that contains date as one column and other columns representing sedimentation per location 
        
    threshold_water : int
        this theshold is used to filter the pixels/positions based on the mean value of the sediment values.
        default value is 5. if the sediment values are lower than this treshold, it is classified as waters.
        
    threshold_land : int
    this theshold is used to filter the pixels/positions based on the percentage of NaNs.
    default value is 80. if the percetange of NaNs are higher than this treshold, it is classified as land.    
    
    Returns
    -------
    df_relevant : DataFrame
        A subset of dataframe/areas where sediment actually appears. So the land and the ocean areas are excluded
    """
  
  df_index = pd.DataFrame() # create an emopty dataframe

  df1 = df.drop(['DateTime'], axis=1)

  # calculate mean 
  df_index['mean'] = df1.mean(axis = 0, skipna=True)
  df_index['missing'] = df1.isnull().sum() * 100 / len(df1) # represents xx percentage of the values are NaNs

  # replace the mean with NaNs, if the percentage of NaNs for the locaton exceeds 80%
  df_index.loc[df_index['missing'] > threshold_land, 'mean'] = float('nan') # if the percentage of NaN higher than 80%, then mean is NaN
  
  # drop the pixel/positions that are either land or considered as waters
  columns_to_drop = list(df_index[df_index['mean'] < threshold_water].index) + list(df_index[np.isnan(df_index['mean']) == True].index)
  df_relevant = df.drop(columns_to_drop, axis = 1)  

  return df_relevant


def plot_positions(df_all_dates): # year = '', location = []  # need to add year and location, for demo
    """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DataFrame
        a dataframe that contains all dates and each position with the sediment value as the column
    Returns
    -------
    plt : plot
        a plot where each line represents the time series for sendiment 
    """
    select_col = [col for col in result.columns if col != 'DateTime'] # if plotting all columns

    df_all_dates.plot(x='DateTime', y= select_col, figsize=(10,5), grid=True)
    
    plt.title('sediment per location over time')
    plt.savefig('sediment_per_location_overtime.jpg')
    
    return plt.show(). # can you return plt.show()?
  

# to-do

# def monthly_average():
# use smoothing to generate the monthly average, so there is no absent values
# if there is still missing values, do interpolation 
# df_interpolate = df.drop(['DateTime'], axis = 1)
# df_interpolated = df_interpolate.interpolate(method ='linear', limit_direction ='forward')
# df_new = pd.concat([df[['DateTime']], df_interpolated], axis = 1)
# df_clean = df_new.dropna()

def sediment_average_over_time(df):
  """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DataFrame
        a dataframe that contains all dates and each position with the sediment value as the column
    Returns
    -------
    df_average : DataFrame
        a dataFrame that represents the average sedimentation over time, with the index of date 
    
    """
  
  df['mean'] = df.drop('DateTime', axis=1).apply(lambda x: x.mean(), axis=1)
  #img = df.plot(x='DateTime', y= 'mean', figsize=(10,5), grid=True)
  df = df.set_index('DateTime')
  df_average = df[['mean']]
  
  return df_average

  
