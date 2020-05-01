# the missing dates are filled in, with a cycle of every 5 days

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta 
from sediment_all_positions import read_data

root_dir = '/data/results/batch_run'
#df = read_data(root_dir, variable = 'spm_nechad2016', nlats = 2946, nlons = 2718)


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

    no_circles = int((df['DateTime'].iloc[-1] - df['DateTime'].iloc[1]) / timedelta(days=5)) + 1

    all_time = []
    for i in range(no_circles):
        temp = df['DateTime'].iloc[1] + i * timedelta(days=5)
        all_time.append(temp)
        df_new = pd.DataFrame(all_time, columns =['DateTime'])

    df_all_dates = pd.merge(df_new, df, on='DateTime', how = 'left') 
    
    return df_all_dates
