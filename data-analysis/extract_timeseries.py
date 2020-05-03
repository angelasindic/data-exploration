import numpy as np
import warnings
import read_netcdf_results

def clean(time_data):
    """Sets negative and very high values to nan. Operates in place!! """
    time_data[time_data < 0.001] = np.nan
    time_data[time_data > 10000] = np.nan

def print_stats(time_data):
    print(f"number of nans: {time_data[np.isnan(time_data)].count()}")
    mean_values = np.nanmean(time_data, axis=0)
    min_values = np.nanmin(time_data, axis=0)
    max_values = np.nanmax(time_data, axis=0)

    # min_values = np.nan_to_num(min_values)
    print(f"min: {np.nanmin(min_values.flatten(), axis=0)}")
    print(f"max: {np.nanmax(max_values.flatten(), axis=0)}")
    print(f"mean: {np.nanmean(mean_values.flatten(), axis=0)}")


def determine_thres(values):

    data = np.ndarray.copy(values)

    print(f"nan values in data: {data[np.isnan(data)].count()}")

    hv = data[np.logical_not(np.isnan(data))]
    print(f"nan values should now be zero: {hv[np.isnan(hv)].count()}")
    print(f"nan values stay same in data: {data[np.isnan(data)].count()}")

    print(f"size: {hv.size}\n std: {np.std(hv)}, mean: {np.mean(hv)}, meadian: {np.median(hv)}, max: {np.max(hv)}, min: {np.min(hv)}")
    print(f"count  < mean: {hv[hv <= np.mean(hv)].count()}, count > mean + std: {hv[hv > np.mean(hv) + np.std(hv)].count()}")
    print(f"rel mean: {hv[hv <= np.median(hv)].count() / hv.size}, rel mean+std {(hv[hv > (np.median(hv) + np.std(hv))].count()) / hv.size}")
    thres = np.mean(hv) + np.std(hv)

    data[np.isnan(data)] = 0.
    data[data < thres] = 0.
    indices = np.argwhere(data)
    return thres, indices, data


def extract_data(time_data, indices):
    i,j = indices[0]
    print(i, j)
    print(time_data[:,i,j])
    ts = time_data[:,i,j]
    print(ts.shape)
    ts_1 = time_data[:, 2,278]
    print(ts_1.shape)


def plot(data, output, title):
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    plot_data = np.ndarray.copy(data)
    plot_data[np.isnan(plot_data)] = 1
    plot_data[plot_data == 0.] = 1

    fig = plt.imshow(plot_data, norm=LogNorm(1, 100))

    fig.set_cmap(plt.cm.RdBu_r)
    plt.colorbar()
    plt.title(title)
    # of cause not working on vm
    #plt.show()
    plt.savefig(output)
    plt.close('all')

def main():

    ###########################
    ## provide parameter values:
    #root_dir = 'data/l2w'
    root_dir = '/data/results/batch_run'

    date = '' #all dates included.
    algorithm = 'spm_nechad2016'

    #outputdir = '/home/angela/transfer/as'
    outputdir = '/home/eouser/transfer/as'
    ###########################

    dates, values = read_netcdf_results.aggregate_timeline(root_dir, date, algorithm, thres=0.85)

    print_stats(values)
    clean(values)
    # using averaged max

    data = np.nanmax(values, axis=0)

    thres, indices, thres_data = determine_thres(data)
    print(f"thres: {thres}, indices shape: {indices.shape}")
    extract_data(values, indices)

    ####
    # plot
    title = f"Averaged Sedimentation Maximum above Threshold of {str(round(thres, 3))}"
    plot(data, outputdir+ '/thres' + '_max_values.png', 'Averaged Sedimentation Maximum')
    plot(thres_data, outputdir+ '/thres' + '_max_values_masked.png', title)



if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        main()






