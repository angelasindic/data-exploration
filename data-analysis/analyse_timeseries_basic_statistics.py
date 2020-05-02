import numpy as np

from read_netcdf_results import aggregate_timeline

def calculate_basic_stats(dates, values, output_location, nlat = 2946, nlon = 2718):
    # calculate numpy NaN statistics obver the whole timeseries, and save to csv

    ts_min = np.nanmin(values, axis=0)
    ts_max = np.nanmax(values, axis=0)
    ts_mean = np.nanmean(values, axis=0)
    ts_median = np.nanmedian(values, axis=0)
    ts_std = np.nanstd(values, axis=0)
    ts_var = np.nanvar(values, axis=0)

    #ts_min.tofile(output_location+'ts_min.bin')
    #ts_max.tofile(output_location+'ts_max.bin')
    #ts_mean.tofile(output_location+'ts_mean.bin')
    #ts_median.tofile(output_location+'ts_median.bin')
    #ts_std.tofile(output_location+'ts_std.bin')
    #ts_var.tofile(output_location+'ts_var.bin')
    
    print('You can plot: ts_min, ts_max, ts_mean, ts_median, ts_std, ts_var')
    return ts_min, ts_max, ts_mean, ts_median, ts_std, ts_var

    

def plot_basic_stats(statistic, plot_title, outfile_name):

    import matplotlib.pyplot as plt
    fig = plt.imshow(statistic, vmin=np.nanpercentile(statistic, 5), vmax=np.nanpercentile(statistic, 95))
    fig.set_cmap(plt.cm.RdBu_r)
    plt.colorbar()
    plt.title(plot_title)
    # of cause not working on vm
    #plt.show()
    plt.savefig(outfile_name+'.png')
    plt.close()
        
