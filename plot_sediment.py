import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sediment_over_all_time.csv')

df['interpolate'] = df['sediment(km2)'].interpolate()

plt.figure(figsize=(20,10))
plt.title('total km quares of sediment from 2018-05-01 to 2020-04-05')
plt.xticks(rotation=90)

plt.plot(df['DateTime'], df['interpolate'])

# https://stackoverflow.com/questions/31590184/plot-multicolored-line-based-on-conditional-in-python
# could plot the interpolated part in a different colour

