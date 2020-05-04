import numpy as np
from numpy import genfromtxt
import warnings
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def read_values(path, shape=(2946, 2718)):
    indices = genfromtxt(path, delimiter=',', dtype='int32')
    print(indices.shape)
    print(indices[:10])
    print(indices[10,0])
    grid = np.zeros(shape)
    for index in range(indices.shape[0]):
        i,j = indices[index]
        grid[i, j] = 1
    return grid


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

def cluster(X, number_of_clusters):

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    pred_y = kmeans.fit_predict(X)

    return pred_y

def get_groups(X, y_km, nc):
    groups = {}
    for c in range(nc):
        print(f"get group for cluster {c}")
        groups[c] = X[y_km == 2]
    return groups

def main():

    ###########################
    ## provide parameter values:

    outputdir = '/home/angela/transfer/as'
    #outputdir = '/home/eouser/transfer/as'
    number_of_clusters = 8
    ###########################

    indices = genfromtxt(outputdir+'/indices.csv', delimiter=',', dtype='int32')


    yPred = cluster(indices, number_of_clusters)
    groups = get_groups(indices, yPred, number_of_clusters)
    print(f"groups: {groups}")
    plot_scatter(indices, yPred, number_of_clusters, outputdir)




# if __name__ == "__main__":
#     with warnings.catch_warnings():
#          warnings.simplefilter("ignore", category=RuntimeWarning)
#         main()

