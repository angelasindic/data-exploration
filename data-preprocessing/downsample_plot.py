import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_total = pd.read_csv('df_mean_std_missing')


image_mean = np.array(df_total['mean']).reshape([2946, 2718])


def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

down_sampled = rebin(image_mean, [491, 453])  # down_sampled to 60m  * 60m, equivalent to reef site size

# make a color map of fixed colors
cmap = mpl.colors.ListedColormap(['blue','green','red'])
bounds=[0,5,15,50]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
plt.imshow(down_sampled, #[0:50, 200:250], #interpolation='nearest',
                    cmap = cmap,norm=norm)

# make a color bar of the mean sedimentation values
plt.colorbar(img,cmap=cmap,
                norm=norm,boundaries=bounds,ticks=[5,15,50])

plt.savefig('image.jpg')
plt.show()
plt.title('mean sediment over time')
