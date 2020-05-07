import numpy as np
from numpy import genfromtxt
import warnings
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# def read_values(path, shape=(2946, 2718)):
#     indices = genfromtxt(path, delimiter=',', dtype='int32')
#     grid = np.zeros(shape)
#     for index in range(indices.shape[0]):
#         i,j = indices[index]
#         grid[i, j] = 1
#     return grid


#shape =(2946, 2718)
def to_grid(indices, shape):
    grid = np.zeros(shape)
    for index in range(indices.shape[0]):
        i,j = indices[index]
        grid[i, j] = 1
    return grid


def median_flter(X, grid_shape, kernel_size):
    import scipy.signal
    grid = to_grid(X, grid_shape)
    filtered = scipy.signal.medfilt(grid, kernel_size=kernel_size)
    result = np.argwhere(filtered)
    return result


def kmeans(X, number_of_clusters):

    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    return kmeans.fit_predict(X)


def cluster(X, grid_shape, kernal_size, number_of_clusters):
    """
    Uses kmeans clustering with the given number of centroids.

     Parameters
    ----------
    X: 2 dim array of values

    Returns
    -------
    array
        Prediction of kmeans
    """
    indices = median_flter(X, grid_shape, kernal_size)
    y_pred = kmeans(indices, number_of_clusters)
    groups = get_groups(indices, y_pred, number_of_clusters)
    return groups


def get_groups(X, y_km, nc):
    groups = {}
    for c in range(nc):
        #print(f"get group for cluster {c}")
        groups[c] = X[y_km == c]
    return groups


def plot_scatter(X, y_km, nc, output):
    palette = ['green', 'orange', 'brown', 'dodgerblue', 'lightblue', 'yellow', 'red', 'blue']
    plt.scatter(X[:, 1], X[:, 0]*-1, c='white', marker='o', edgecolor='black', s=5)

    for c in range(nc):
        plt.scatter(
            X[y_km == c, 1], X[y_km == c, 0]*-1,
            s=50, c=palette[c],
            marker='+',
            label='cluster'+ '_'+ str(c)
        )

    plt.savefig(output+ '/max_cluster.png')
    plt.close('all')

def plot(groups, output):
    palette = ['green', 'orange', 'brown', 'dodgerblue', 'lightblue', 'yellow', 'red', 'blue']
    for cluster, cluster_indices in groups.items():
        plt.scatter(cluster_indices[:, 1], cluster_indices[:, 0]*-1,
            s=10, c=palette[cluster], marker= '+',
            label = 'cluster' + '_' + str(cluster))
    plt.savefig(output + '/max_cluster.png')
    plt.close('all')

def plot_grid(groups, grid_shape, output):
    import matplotlib.pyplot as plt
    from matplotlib import colors

    # make a color map of fixed colors
    grid = np.zeros(grid_shape)
    for group, g_indices in groups.items():
        for index in range(g_indices.shape[0]):
            i, j = g_indices[index]
            grid[i, j] = group+1

    cmap = colors.ListedColormap(['white', 'orange', 'brown', 'dodgerblue', 'lightblue', 'yellow', 'red', 'blue'])
    #bounds = [0, 1, 2]
    bounds = range(len(groups)+2)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # tell imshow about color map so that only set colors are used
    # img = plt.imshow(f_grid, interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
    img = plt.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)

    # make a color bar
    plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0, 5, 10])

    plt.savefig(output)
    plt.close('all')


def main():

    ###########################
    ## provide parameter values:

    outputdir = '/home/angela/transfer/as'
    #outputdir = '/home/eouser/transfer/as'
    number_of_clusters = 8
    ###########################

    indices = genfromtxt(outputdir+'/indices.csv', delimiter=',', dtype='int32')


    yPred = kmeans(indices, number_of_clusters)
    groups = get_groups(indices, yPred, number_of_clusters)
    print(f"groups: {groups}")
    plot_scatter(indices, yPred, number_of_clusters, outputdir)


# if __name__ == "__main__":
#     with warnings.catch_warnings():
#          warnings.simplefilter("ignore", category=RuntimeWarning)
#         main()

def define_number_of_clusters(grid):

    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(grid)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, 11), wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()