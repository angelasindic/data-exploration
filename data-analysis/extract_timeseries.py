import numpy as np
import warnings
import read_netcdf_results, clustering

def clean(time_data):
    """Sets negative and very high values to nan. Operates in place!! """
    time_data[time_data < 0.001] = np.nan
    time_data[time_data > 10000] = np.nan

def print_stats(time_data):
    print(f"number of nans: {time_data[np.isnan(time_data)].count()}")
    mean_values = np.nanmean(time_data, axis=0)
    min_values = np.nanmin(time_data, axis=0)
    max_values = np.nanmax(time_data, axis=0)
    std_values = np.nanstd(time_data, axis=0)

    min = np.nanmedian(min_values.flatten(), axis=0)
    max = np.nanmedian(max_values.flatten(), axis=0)
    mean = np.nanmedian(mean_values.flatten(), axis=0)
    std = np.nanmedian(std_values.flatten(), axis=0)



    return min, max, mean, std


def determine_thres(values):

    data = np.ndarray.copy(values)

    print(f"nan values in data: {data[np.isnan(data)].count()}")

    hv = data[np.logical_not(np.isnan(data))]
    #print(f"nan values should now be zero: {hv[np.isnan(hv)].count()}")
    #print(f"nan values stay same in data: {data[np.isnan(data)].count()}")

    print(f"non nan values in data: {hv.size}\n std: {np.std(hv)}, mean: {np.mean(hv)}, meadian: {np.median(hv)}, max: {np.max(hv)}, min: {np.min(hv)}")
    print(f"count  < mean: {hv[hv <= np.mean(hv)].count()}, count > mean + std: {hv[hv > np.mean(hv) + np.std(hv)].count()}")
    print(f"rel mean: {hv[hv <= np.median(hv)].count() / hv.size}, rel mean+std {(hv[hv > (np.median(hv) + np.std(hv))].count()) / hv.size}")

    thres = 2 * np.mean(hv)

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

def save_as_csv(values, output):
    np.savetxt(output, values, delimiter=",")

def read_from_csv(path):
    from numpy import genfromtxt
    return genfromtxt(path, delimiter=',')

#from sklearn.cluster import KMeans
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
    plt.savefig(output)
    plt.close('all')

def main():

    ###########################
    ## provide parameter values:

    #root_dir = 'data/l2w'
    root_dir = '/data/results/batch_run'

    date = '' #all dates included.
    algorithm = 'spm_nechad2016'

    #outputdir = '/home/angela/transfer/as/local'
    outputdir = '/home/eouser/transfer/as'

    kernel_size = 7
    number_of_clusters = 3
    ###########################

    dates, values = read_netcdf_results.aggregate_timeline(root_dir, date, algorithm, thres=0.85)

    min, max, mean, std = print_stats(values)
    print(f"min: {min}")
    print(f"max: {max}")
    print(f"mean: {mean}")
    print(f"std: {std}")

    clean(values)

    # using averaged max
    data = np.nanmax(values, axis=0)

    thres, indices, thres_data = determine_thres(data)
    print(f"Thresolding data with: {thres}, indices shape: {indices.shape}")

    ### clustering
    print(f"Clustering with indices of size: {indices.shape}")
    groups = clustering.cluster(indices, data.shape, kernal_size=kernel_size, number_of_clusters=number_of_clusters)


    ##extract dataframe per group and save it as csv
    for cluster, cluster_indices in groups.items():

        cluster_values = values[:, cluster_indices[:, 0], cluster_indices[:, 1]]
        print(f"selection of size: {cluster_values.shape}")

        df = read_netcdf_results.convert_to_dataframe(dates, cluster_values, thres_col=0.)
        df.to_csv(outputdir + '/df_cluster_'+ str(cluster) + '.csv')


    print("plotting and saveing intermediate results")
    save_as_csv(indices, outputdir + '/indices.csv')
    plot(data, outputdir + '/thres_max_values.png', 'Averaged Sedimentation Maximum')

    title = f"Averaged Sedimentation Maximum masked with {str(round(thres, 3))}"
    filename = f"{outputdir}/thres_max_values_masked_{str(round(thres))}.png"
    plot(thres_data, filename, title)

    clustering.plot(groups, outputdir)
    clustering.plot_grid(groups, data.shape, outputdir + '/max_clusters.png')



if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        main()






