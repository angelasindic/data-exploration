# downsample the image based on the mean of each position, by a degree of 6-> 60m*60m
   # -> appximate coral outplanting site ~3000 m2
# also because both dimensions [2946, 2718] are divisbile by 6
# need to fix about the coastline, since after downsampling, some lands close to coastlines will be classified as water.
   # not a big issue: false positive not expensive here, they will not plant corals on land!
# colour scale: red--> high sediment, green --> low sediment, blue --> no sediment
# need to mask the land aresa with all NaNs

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sediment_all_positions import read_data
from add_dates import add_dates
from stats import stats_custom

root_dir = '/data/results/batch_run'
#df = read_data(root_dir, variable = 'spm_nechad2016', nlats = 2946, nlons = 2718)
#df_all_dates = add_dates(df)
#df_total = stats_custom(df)

#df_total = pd.read_csv('df_mean_std_missing')

def down_sample(df, degree = 6):
   
   """
    Summary line.
    Extended description of function.
    Parameters
    ----------
    df : DateFrame
        the dataframe that contains mean, std of sedimentation and percentage of NaNs per location 
    
    degree : int
        down-sampling degree. Default is 6
    
    Returns
    -------
    (image_mean_down, image_std_down)
        turple of 2-d arrays, each representing the downsampled mean and std
    """
   
   image_mean = np.array(df['mean']).reshape([2946, 2718])
   image_std = np.array(df['std']).reshape([2946, 2718])

   
   shape = [2946 // degree, 2718 // degree]
   
   def rebin(a, shape):
       sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
       return a.reshape(sh).mean(-1).mean(1)

   # down_sampled to 60m  * 60m, equivalent to reef site size
   image_mean_down = rebin(image_mean, shape)   
   image_std_down = rebin(image_std, shape)  

   return image_mean_down, image_std_down


# make a color map of fixed colors
# first plot the image of how std changes across locations
cmap = mpl.colors.ListedColormap(['blue','green','red'])
bounds=[0,5,15,50]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
img = plt.imshow(image_std, #[0:50, 200:250], #interpolation='nearest',
                    cmap = cmap,norm=norm)

# make a color bar of the std sedimentation values
plt.colorbar(img,cmap=cmap,
                norm=norm,boundaries=bounds,ticks=[5,15,50])

plt.savefig('image_std.jpg')
plt.show()
plt.title('mean sediment over time')
