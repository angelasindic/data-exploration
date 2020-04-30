import numpy as np

from read_netcdf_results import aggregate_timeline, count_nans


def get_best_index(nan_values):
    # Choose 'the best' timeseries: the one with min number of nan values
    print("count nan values for each element per time slice")
    i, j = np.unravel_index(np.argmin(nan_values, axis=None), nan_values.shape)
    print(f"element with min nan values: {i},{j}")
    return i,j


def create_timeseries(dates, values, pos_index):
    import pandas as pd
    # output running
    # i,j = get_best_index(values)
    #### 12,1274 ####

    i,j = pos_index


    #print(f"time series values dim: {values[:, i, j].shape}")
    #print(values[:, i, j])

    # To pick a timeseries slice: values[:,i,j]
    ts = values[:, i, j]
    #print(ts.shape)

    data = np.stack((dates, ts), axis=1)
    #print(data.shape)

    # create time series
    index = pd.DatetimeIndex(dates)
    data = pd.Series(ts, index=index)
    return data


def plot_timeseries_spm(pos_index):
    import matplotlib.pyplot as plt
    import seaborn; seaborn.set()

    dates, values = aggregate_timeline('data/l2w','', 'spm_nechad2016')
    data = create_timeseries(dates, values, pos_index)
    print(data.describe())
    data.plot()
    plt.ylabel('Sedimentation')
    plt.show()

def plot_resampled_timeseries_spm(pos_index, resample):
    import matplotlib.pyplot as plt
    import seaborn; seaborn.set()

    dates, values = aggregate_timeline('data/l2w', '', 'spm_nechad2016')
    data = create_timeseries(dates, values, pos_index)
    print(data.describe())
    month = data.resample(resample).sum()
    month.plot()
    plt.ylabel('Sedimentation')
    plt.show()
