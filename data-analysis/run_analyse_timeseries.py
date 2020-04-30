import analyse_timeseries
import read_netcdf_results

def main():
    ########
    # example: read data from netCDF, count nan values, determin index with min nan values and plot the nan-value.


    ###########################
    ## provide parameter values:
    root_dir = 'data/l2w'
    date = '' #all dates included.
    algorithm = 'spm_nechad2016'
    ###########################

    ###########################
    ## call function
    dates, values = read_netcdf_results.aggregate_timeline(root_dir, date, algorithm)
    ###########################

    print(f"dates: {dates}")
    print(f"values dim: {values.shape}")


    ###########################
    ## call functions
    nan_values = read_netcdf_results.count_nans(values)
    best_index = analyse_timeseries.get_best_index(nan_values)
    print("Index {best_index} has lowest count of nan values: {nan_values[best_index]}")
    ###########################

    ############# plot nan-values array #############

    import matplotlib.pyplot as plt
    fig = plt.imshow(nan_values)
    fig.set_cmap(plt.cm.RdBu_r)
    plt.colorbar()
    plt.ylabel('# NaN Values')
    plt.show()


if __name__ == "__main__":
    main()




#plot_resampled_timeseries_spm(pos_index=(12,1274), resample='M')
#plot_timeseries_spm(pos_index=(12,1274))


