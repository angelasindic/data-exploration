# the missing dates are filled in, with a cycle of every 5 days
# the sediment time series for different positions are plotted together for comparison

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from sediment_all_positions import read_data

df = read_data(root_dir = os.listdir(), nlats = 2946, nlons = 2718) # read in the csv data that has all the sediment

def restrain_area(df, threshold = 5):
  """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DateFrame
        the dataframe that contains date as one column and other columns representing sedimentation per location 
    
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
  df_index.loc[df_index['missing'] > 80, 'mean'] = float('nan') # if the percentage of NaN higher than 80%, then mean is NaN
    
  columns_to_drop = list(df_index[df_index['mean'] < threshold].index) + list(df_index[df_index['mean'] == float('nan')].index)

  df_relevant = df.drop(columns_to_drop, axis = 1)
  
  return df_relevant


def add_dates(df):
    """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DataFrame
        a dataframe that contains date and each position with the sediment value as the column
    Returns
    -------
    result : DataFrame
        A dataframe with all dates with an interval of 5 days --> frequency of sentinel-2 satellite imagery
    """
    
    df['DateTime'] = pd.to_datetime(df['date']) # make sure that this dateframe has bee sorted according to datetime
    df = df.drop(['date'], axis=1).sort_values(["DateTime"], ascending = (True))

    no_circles = int((df['DateTime'].iloc[-1] - df['DateTime'].iloc[1]) / dt.timedelta(days=5)) + 1

    all_time = []
    for i in range(no_circles):
        temp = df['DateTime'].iloc[1] + i * dt.timedelta(days=5)
        all_time.append(temp)
        df_new = pd.DataFrame(all_time, columns =['DateTime'])

    df_all_dates = pd.merge(df_new, df, on='DateTime', how = 'left') 
    
    return df_all_dates

#df_all_dates.to_csv('sediment_per_location_over_all_time.csv')


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
    
    return plt.show()
