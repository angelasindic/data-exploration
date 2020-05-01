# the missing dates are filled in, with a cycle of every 5 days

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

df = pd.read_csv('pd_all_sediment.csv') # read in the csv data that has all the sediment

select_col = [col for col in df.columns if col != 'date']


df['DateTime'] = pd.to_datetime(df['date']) # make sure that this dateframe has bee sorted according to datetime

no_circles = int((df['DateTime'].iloc[-1] - df['DateTime'].iloc[1]) / dt.timedelta(days=5)) + 1

all_time = []
for i in range(no_circles):
    temp = df['DateTime'].iloc[1] + i * dt.timedelta(days=5)
    all_time.append(temp)
    df_new = pd.DataFrame(all_time, columns =['DateTime'])
    
result = pd.merge(df_new, df, on='DateTime', how = 'left') 
#result.to_csv('sediment_per_location_over_all_time.csv')


result.plot(x='DateTime', y= select_col, figsize=(10,5), grid=True)

plt.savefig('sediment_per_location_overtime.jpg')
plt.show()
plt.title('sediment per location over time')
