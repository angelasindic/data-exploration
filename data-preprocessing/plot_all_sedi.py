import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('pd_all_sediment.csv') # read in the csv data that has all the sediment

select_col = [col for col in df.columns if col != 'date']

df.plot(x='date', y= select_col, figsize=(10,5), grid=True)

plt.savefig('sediment_per_location_overtime.jpg')
plt.show()
plt.title('sediment per location over time')
