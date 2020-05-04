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
    max= np.nanmedian(max_values.flatten(), axis=0)
    mean= np.nanmedian(mean_values.flatten(), axis=0)
    std= np.nanmedian(std_values.flatten(), axis=0)

    print(f"min: {min}")
    print(f"max: {max}")
    print(f"mean: {mean}")
    print(f"std: {std}")

    return min, max, mean, std


def determine_thres(values):

    data = np.ndarray.copy(values)

    print(f"nan values in data: {data[np.isnan(data)].count()}")

    hv = data[np.logical_not(np.isnan(data))]
    print(f"nan values should now be zero: {hv[np.isnan(hv)].count()}")
    print(f"nan values stay same in data: {data[np.isnan(data)].count()}")

    print(f"size: {hv.size}\n std: {np.std(hv)}, mean: {np.mean(hv)}, meadian: {np.median(hv)}, max: {np.max(hv)}, min: {np.min(hv)}")
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

    number_of_clusters = 8
    ###########################

    dates, values = read_netcdf_results.aggregate_timeline(root_dir, date, algorithm, thres=0.85)

    print_stats(values)
    clean(values)

    # using averaged max
    data = np.nanmax(values, axis=0)

    thres, indices, thres_data = determine_thres(data)
    print(f"thres: {thres}, indices shape: {indices.shape}")

    ### clustering
    yPred = clustering.cluster(indices, number_of_clusters)
    groups = clustering.get_groups(indices, yPred, number_of_clusters)

    ###
    ##extract dataframe per group and save it as csv
    for cluster, cluster_indices in groups.items():

        cluster_values = values[:, cluster_indices[:, 0], cluster_indices[:, 1]]
        print(f"selection of size: {cluster_values.shape}")

        df = read_netcdf_results.convert_to_dataframe(dates, cluster_values, thres_col=0.)
        df.to_csv(outputdir + '/df_cluster_'+ str(cluster) + '.csv')


    #df['empty_values'] = df.isnull().sum(axis=1)
    #df['median'] = df.median(axis=1)
    #df['mean'] = df.mean(axis=1)

    # plots and save intermediate results
    save_as_csv(indices, outputdir + '/indices.csv')
    plot(data, outputdir + '/thres_max_values.png', 'Averaged Sedimentation Maximum')

    title = f"Averaged Sedimentation Maximum masked with {str(round(thres, 3))}"
    filename = f"{outputdir}/thres_max_values_masked_{str(round(thres))}.png"
    print(filename)
    plot(thres_data, filename, title)

    clustering.plot_scatter(indices, yPred, number_of_clusters, outputdir)



if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        main()






