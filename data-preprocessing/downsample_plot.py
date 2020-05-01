# downsample the image based on the mean of each position, by a degree of 6
# also because both dimensions [2946, 2718] are divisbile by 6
# need to fix about the coastline, since after downsampling, some lands close to coastlines will be classified as water.
   # not a big issue: false positive not expensive here, they will not plant corals on land!
# colour scale: red--> high sediment, green --> low sediment, blue --> no sediment
# need to mask the land aresa with all NaNs

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_total = pd.read_csv('df_mean_std_missing')


image_mean = np.array(df_total['mean']).reshape([2946, 2718])
image_std = np.array(df_total['std']).reshape([2946, 2718])



def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

down_sampled = rebin(image_std, [491, 453])  # down_sampled to 60m  * 60m, equivalent to reef site size

# make a color map of fixed colors
cmap = mpl.colors.ListedColormap(['blue','green','red'])
bounds=[0,5,15,50]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
img = plt.imshow(image_std, #[0:50, 200:250], #interpolation='nearest',
                    cmap = cmap,norm=norm)

# make a color bar of the mean sedimentation values
plt.colorbar(img,cmap=cmap,
                norm=norm,boundaries=bounds,ticks=[5,15,50])

plt.savefig('image_std.jpg')
plt.show()
plt.title('mean sediment over time')
