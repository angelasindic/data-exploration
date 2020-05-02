import numpy as np

def determine_thres(time_data):
    print(f"number of nans: {time_data[np.isnan(time_data)].count()}")
    time_data[time_data < 0.001] = np.nan
    time_data[time_data > 10000] = np.nan
    mean_values = np.nanmean(time_data, axis=0)
    min_values = np.nanmin(time_data, axis=0)

    # this is used for extracting
    max_values = np.nanmax(time_data, axis=0)

    nan_count = min_values[np.isnan(min_values)].count()
    print(f"nan_count: {nan_count}")
    # min_values = np.nan_to_num(min_values)
    print(f"min: {np.nanmin(min_values.flatten(), axis=0)}")
    print(f"max: {np.nanmax(max_values.flatten(), axis=0)}")
    print(f"mean: {np.nanmean(mean_values.flatten(), axis=0)}")

    data = max_values

    print(f"nan values in max data: {data[np.isnan(data)].count()}")

    hv = data[np.logical_not(np.isnan(data))]
    print(f"nan values should now be zero: {hv[np.isnan(hv)].count()}")

    print(f"size: {hv.size}\n std: {np.std(hv)}, mean: {np.mean(hv)}, meadian: {np.median(hv)}, max: {np.max(hv)}, min: {np.min(hv)}")
    print(f"count  < mean: {hv[hv <= np.mean(hv)].count()}, count > mean + std: {hv[hv > np.mean(hv) + np.std(hv)].count()}")
    print(f"rel mean: {hv[hv <= np.median(hv)].count() / hv.size}, rel mean+std {(hv[hv > (np.median(hv) + np.std(hv))].count()) / hv.size}")
    thres = np.mean(hv) + np.std(hv)
    return hv, thres




