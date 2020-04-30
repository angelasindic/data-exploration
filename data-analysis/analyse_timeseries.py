import numpy as np
from read_netcdf_results import aggregate_timeline, count_nans


def get_index_for_timeseries(values):
    # Choose 'the best' timeseriese, the one with min number of nan values
    print("count nan values for each element per time slice")
    nan_values = count_nans(values)
    i, j = np.unravel_index(np.argmin(nan_values, axis=None), nan_values.shape)
    print(f"element with min nan values: {i},{j}")
    return i,j


def create_timeseries():
    import pandas as pd
    dates, values = aggregate_timeline('', 'spm_nechad2016')
    print(f"stacked values dim: {values.shape}")

    # output running
    # i,j = get_index_for_timeseries(values)
    #### 12,1274 ####

    i = 12
    j = 1274
    # To pick a timeseries slice: values[:,i,j]
    print(f"time series values dim: {values[:, i, j].shape}")
    print(values[:, i, j])

    ts = values[:, i, j]
    print(ts.shape)
    # npa = np.asarray(someListOfLists, dtype=np.float32)
    # npa = np.asarray(dates)
    data = np.stack((dates, ts), axis=1)
    print(data.shape)
    # create time series
    index = pd.DatetimeIndex(dates)
    data = pd.Series(ts, index=index)
    return data

def plot_timeseries(resample='M'):
    #% matplotlib inline
    import matplotlib.pyplot as plt
    import seaborn; seaborn.set()

    data = create_timeseries()
    print(data.describe())
    month = data.resample(resample).sum()
    month.plot()
    plt.ylabel('Sedimentation');
    plt.show()


