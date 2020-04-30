#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import glob
import pandas as pd
from netCDF4 import Dataset
import numpy as np


# In[2]:


import os
import pandas as pd
import rasterio as rio
import matplotlib.pyplot as plt
#from rasterio.plot import show
import numpy as np
from PIL import Image
#from imageio import imread


# In[3]:


os.chdir('/Users/wentingjiang/PycharmProjects/)


# In[525]:


os.getcwd()


# In[4]:


os.chdir('/Users/wentingjiang/PycharmProjects/coraladies')


# In[473]:


data_temp.shape


# In[5]:


df = pd.DataFrame()
for folder_name in os.listdir():
    if '-' in folder_name: 
        for file_name in glob.glob(os.getcwd()+ '/' + folder_name + '/*L2W.nc'):
            nc = Dataset(file_name)
            ds = list(nc.variables.keys())
            dataset = ds[3] 
            data_temp = nc.variables[dataset][:]
            data = data_temp.flatten('C')
            data_split = np.ma.hsplit(data, 1)
            df_temp = pd.DataFrame(data_split)
            df_temp['date'] = folder_name
            df = pd.concat([df, df_temp])

df.to_csv('pd_all_sediment.csv', index=False)  

#df_small.to_csv('pd_sediment_small.csv', index=False)      


# In[15]:


## calculate mean and standard

df = pd.read_csv('pd_all_sediment.csv')

df1 = df.drop(['date'], axis=1)
df2 = df1.mean(axis = 0, skipna=True)

df3 = df1.std(axis = 0, skipna=True)

df_total = pd.DataFrame()
df_total['mean'] = df2
df_total['std'] = df3

# calculate percentage of missing values

percent_missing = df1.isnull().sum() * 100 / len(df1)
df_total['missing'] = percent_missing

#image_mean = np.array(df_total['mean']).reshape(data_temp.shape)


# In[16]:


df_total = pd.DataFrame()


# In[17]:


df_total['mean'] = df2


# In[18]:


df_total['std'] = df3


# In[26]:


df1


# In[27]:


percent_missing = df1.isnull().sum() * 100 / len(df1)


# In[29]:


df_total['missing'] = percent_missing


# In[30]:


#df_total.to_csv('df_mean_std_missing', index = False)


# In[31]:


# reshape in order to plot

image_mean = np.array(df_total['mean']).reshape(data_temp.shape)


# In[20]:


image_mean.shape


# In[591]:


2718/6


# In[589]:


## downsample the mean


# In[21]:


def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)


# In[22]:


down_sampled = rebin(image_mean, [491, 453])


# In[23]:


down_sampled


# In[600]:


np.nanmean(down_sampled)


# In[601]:


np.nanmax(down_sampled)


# In[602]:


np.nanmin(down_sampled)


# In[38]:


import matplotlib as mpl
from matplotlib import pyplot
import numpy as np


# make a color map of fixed colors
cmap = mpl.colors.ListedColormap(['blue','green','red'])
bounds=[0,5,15,50]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
img = pyplot.imshow(down_sampled, #[0:50, 200:250], #interpolation='nearest',
                    cmap = cmap,norm=norm)

# make a color bar of the mean sedimentation values
pyplot.colorbar(img,cmap=cmap,
                norm=norm,boundaries=bounds,ticks=[5,15,50])

pyplot.show()


# In[593]:


fig, ax = plt.subplots()
im = ax.imshow(down_sampled) 
fig.colorbar(im, ax=ax)
ax.set_title('variance of the sediment density over time')


# In[586]:


fig, ax = plt.subplots()
im = ax.imshow(image_mean) 
fig.colorbar(im, ax=ax)
ax.set_title('variance of the sediment density over time')


# In[565]:


type(df2)


# In[552]:


df.shape


# In[329]:


data.reshape(data_temp.shape) == data_temp


# In[557]:


fig, ax = plt.subplots()
im = ax.imshow(data_temp) 
fig.colorbar(im, ax=ax)
ax.set_title('variance of the sediment density over time')


# In[556]:


fig, ax = plt.subplots()
im = ax.imshow(data_temp) 
fig.colorbar(im, ax=ax)
ax.set_title('mean of the sediment density over time')

print('the mean sediment is... the variance is...')
print('the percentage of the data is missing')

# when they look into each pixel (with a specified round of meters), the detailed trend/average trend for the area
# will show up


# In[482]:


fig, ax = plt.subplots()
im = ax.imshow(data_temp2) 
fig.colorbar(im, ax=ax)


# In[266]:


data = data_temp.flatten('C')


# In[271]:


data.shape


# In[249]:


test = data_temp[200, :]


# In[251]:


test.ndim


# In[246]:


#df['test'] =test


# In[272]:


test = pd.DataFrame(data)


# In[273]:


test['rv'] = test.rolling(window=5, min_periods=2).mean()


# In[275]:


test


# In[274]:


test.isna().sum()


# In[264]:


df['rv'].isna().sum()


# In[235]:


np.nanmean(test)


# In[501]:


os.chdir('/Users/wentingjiang/PycharmProjects')


# In[502]:


df = pd.read_csv('pd_sediment_small.csv')


# In[503]:


df = df.drop_duplicates()


# In[504]:


df2 = pd.read_csv('pd_sediment_small2.csv')


# In[505]:


df2 = df2.drop_duplicates(keep=False)


# In[506]:


df2.shape


# In[507]:


df_join = df2.merge(df, how = 'left', on = 'date')


# In[508]:


df_join


# In[509]:


df = df_join.sort_values(by=['date'])


# In[510]:


df.columns


# In[469]:


position2 = ['89980', '89981', '89982', '89983', '89984', '89985', '89986',
       '89987', '89988', '89989', '89990', '89991', '89992', '89993', '89994',
       '89995', '89996', '89997', '89998', '89999']

position1 = ['59981', '59982', '59983',
       '59984', '59985', '59986', '59987', '59988', '59989', '59990', '59991',
       '59992', '59993', '59994', '59995', '59996', '59997', '59998', '59999']


# In[522]:


# how to plot multiple images in one big image

fig, axs = plt.subplots(2, 2)

axs[0, 0].plot(df['date'], df[position1]) #figsize=(10,5), grid=True)
axs[0, 0].set_title('sediment in position1')
axs[0, 1].imshow(data_temp)
axs[0, 1].set_title('current image of position1')
axs[1, 0].plot(df['date'], df[position2])
axs[1, 0].set_title('sediment in position2')
axs[1, 1].imshow(data_temp2)
axs[1, 1].set_title('current image of position2')

for ax in axs.flat:
    ax.label_outer()


# In[471]:


df.plot(x='date', y= position1, figsize=(10,5), grid=True)


# In[470]:


df.plot(x='date', y= position2, figsize=(10,5), grid=True)


# In[388]:


#df_short = df.iloc[-50:,:]


# In[389]:


df_interpolate = df_short.drop(['date'], axis = 1)


# In[390]:


df_interpolated = df_interpolate.interpolate(method ='linear', limit_direction ='forward')


# In[391]:


df_interpolated


# In[ ]:





# In[392]:


#pd.concat([df1, df4.reindex(df1.index)], axis=1)

df_new = pd.concat([df_short[['date']], df_interpolated], axis = 1)


# In[393]:


df_clean = df_new.dropna()


# In[398]:


df_clean


# In[399]:


df_clean['mean'] = df_clean.drop('date', axis=1).apply(lambda x: x.mean(), axis=1)


# In[401]:


df_clean


# In[360]:


df_clean.plot(x='date', y= position, figsize=(10,5), grid=True)


# In[409]:


from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm


# In[402]:


df_clean.plot(x='date', y= 'mean', figsize=(10,5), grid=True)


# In[416]:


df_clean = df_clean.set_index('date')
#s=sm.tsa.seasonal_decompose(df.mean)


# In[419]:


df = df_clean[['mean']]


# In[420]:


df


# In[421]:


seasonal_decompose(df[['mean']], model='additive', freq=1).plot()


# In[ ]:


import statsmodels.api as sm

dta = sm.datasets.co2.load_pandas().data
# deal with missing values. see issue
dta.co2.interpolate(inplace=True)

res = sm.tsa.seasonal_decompose(dta.co2)
resplot = res.plot()


# In[ ]:





# In[ ]:





# In[361]:


df_short.plot(x='date', y= position, figsize=(10,5), grid=True)


# In[296]:


df_short.columns


# In[300]:


df_short.plot(x='date', y= position, figsize=(10,5), grid=True)


# In[ ]:




