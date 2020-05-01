import numpy as np

from read_netcdf_results import aggregate_timeline

def calculate_basic_stats(dates, values, nlat = 2946, nlon = 2718, output_location=root_dir,):
    # calculate numpy NaN statistics obver the whole timeseries, and save to csv

    idx = len(dates)
    tur=np.empty((idx))

    ts_max=np.empty((nlat//2,nlon//2))
    ts_min=np.empty((nlat//2,nlon//2))
    ts_mean=np.empty((nlat//2,nlon//2))
    ts_median=np.empty((nlat//2,nlon//2))
    ts_std=np.empty((nlat//2,nlon//2))
    ts_var=np.empty((nlat//2,nlon//2))


    for i in range(nlon//2):
      for j in range(nlat//2):
        tur[:] = values[0:idx,j,i]
        loc_min = np.nanmin(tur)
        loc_max = np.nanmax(tur)
        loc_mean = np.nanmean(tur)
        loc_median = np.nanmedian(tur)
        loc_std = np.nanstd(tur)
        loc_var = np.nanvar(tur)
        ts_min[j,i] = loc_min
        ts_max[j,i] = loc_max
        ts_mean[j,i] = loc_mean
        ts_median[j,i] = loc_median
        ts_std[j,i] = loc_std
        ts_var[j,i] = loc_var

    ts_min.tofile(output_location+'ts_min.bin')
    ts_max.tofile(output_location+'ts_max.bin')
    ts_mean.tofile(output_location+'ts_mean.bin')
    ts_meadian.tofile(output_location+'ts_median.bin')
    ts_std.tofile(output_location+'ts_std.bin')
    ts_var.tofile(output_location+'ts_var.bin')
    
    print('You can plot: ts_min, ts_max, ts_mean, ts_median, ts_std, ts_var')
    return ts_min, ts_max, ts_mean, ts_median, ts_std, ts_var

    

def plot_basic_stats(statistic, plot_title, outfile_name):

    import matplotlib.pyplot as plt
    fig = plt.imshow(glob_statistic, clim=(0.0,10.0))
    fig.set_cmap(plt.cm.RdBu_r)
    plt.colorbar()
    plt.title(plot_title)
    # of cause not working on vm
    #plt.show()
    plt.savefig(outfile_name+'.png')
        
