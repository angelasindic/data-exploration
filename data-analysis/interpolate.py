import numpy as np
from read_netcdf_results import get_products, count_nans

def interpolate(filename, algorithm, factor, order):
    from mpl_toolkits import basemap
    from netCDF4 import Dataset

    with Dataset(filename, mode='r') as fh:
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        values = fh.variables[algorithm][:].squeeze()

    lats_sorted = np.sort(lats, axis=0)
    lons_sorted = np.sort(lons, axis=0)
    lons_new, lats_new = np.meshgrid(lons_sorted[0, :][::factor], lats_sorted[:, 0][::factor])

    print(lats_new.shape)
    print(lons_new.shape)
    values_coarse = basemap.interp(values, lons_sorted[0, :], lats_sorted[:, 0], lons_new, lats_new, order=order)
    print(f"min: {np.nanmin(values_coarse)}, max: {np.nanmax(values_coarse)}, mean: {np.nanmean(values_coarse)}")
    return values_coarse, lons_new, lats_new


def aggregate_values(root_dir, date, algorithm, factor, order):
    filenames = get_products(root_dir, date)
    v_list = []
    for filename in filenames:
        v, _, _ = interpolate(filename, algorithm, factor, order)
        v_list.append(v)
    values = np.stack(v_list, axis=0)
    print(values.shape)
    return values


def main():
    #root_dir = 'data/l2w'
    root_dir = '/data/results/batch_run'
    date = '' #all dates included.
    algorithm = 'spm_nechad2016'
    factor = 50
    order = 0
    values = aggregate_values(root_dir, date, algorithm, factor, order)
    ###########################
    ## call functions
    nan_values = count_nans(values)
    print(f'nan values, min: {np.min(nan_values)}, max: {np.max(nan_values)}, {np.mean(nan_values)}')
    ###########################

    ############# plot nan-values array #############

    import matplotlib.pyplot as plt
    fig = plt.imshow(nan_values)
    fig.set_cmap(plt.cm.RdBu_r)
    plt.colorbar()
    plt.ylabel('# NaN Values')
    # of cause not working on vm
    # plt.show()
    plt.savefig('nan_values_interpolated_50.png')



if __name__ == "__main__":
    # execute only if run as a script
    main()
