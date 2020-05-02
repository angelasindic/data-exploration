
######### NOT cleaned up yet #########

from matplotlib.pyplot import legend
import sys

# get weather: precipation
df_weather = pd.read_csv('golfito.csv')
df_weather = df_weather.rename(columns = {'date_time': 'DateTime'})
df_merge = df_weather.merge(df, how = 'left', on = 'DateTime')
data2 = df_merge['precipMM']

# get the sedimentation areas
df['interpolate'] = df['sediment(km2)'].interpolate()
series = df[['DateTime','interpolate']]
series.set_index('DateTime', inplace=True)

# plot them both
fig,ax = plt.subplots()
ax2=ax.twinx()
s1mask = np.isfinite(series1)
ax.plot(series1[s1mask], linestyle='-', marker='o', color = 'green', label = 'sediment')
ax2.plot(data2, color='red')

plt.figure(figsize=(20,10))
plt.xticks(rotation=90)

#legend((line1, line2), ('sediment', 'precipation'))
plt.show()
