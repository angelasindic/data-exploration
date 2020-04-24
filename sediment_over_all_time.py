#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime as dt
import pandas as pd

df = pd.read_csv('sediment_over_time.csv')
df['DateTime'] = pd.to_datetime(df['date'])

no_circles = int((df['DateTime'].iloc[-1] - df['DateTime'].iloc[1]) / dt.timedelta(days=5)) + 1

all_time = []
for i in range(no_circles):
    temp = df['DateTime'].iloc[1] + i * dt.timedelta(days=5)
    all_time.append(temp)
    df_new = pd.DataFrame(all_time, columns =['DateTime'])
    

result = pd.merge(df_new, df, on='DateTime', how = 'left') 
result.to_csv('sediment_over_all_time.csv')

