to view the damo, open the jupyter notebook, read in the csv files (position1, position2), and use 'voila' tab inside jupyter to launch demo

there is another csv file required for demo, which is too big to upload to github.
--> name of the file is "df_mean_std_missing", it can be downloaded from VM in the directory:  --> cd /data/results/batch_run

The final version of demo is from this notebook: demo-killer-featuer.ipynb

# Steps to generate the time series plot of a particular location

# 1. Find index of the position
based on the latitude, longitude of interest, find the respective index in the big dataframe

 --> big dataframe is a concated df where each column (after being flattened from 2d array to 1d) represents a location 
 
 --> users' input for latitude and longitude are stored in these two variables: corals_latitude.value, corals_longitude.value
 
 --> because the original 2d array was flattend using the 'C' method, which flattens the 2d array row by row (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.flatten.html)
     inversely, we can find the idx of the position in the big dataframe with the formula below
     idx = (int(corals_latitude.value) - 1) * 2718 + int(corals_longitude.value) 
 
# 2. Query the position's sediment values from VM
use the index above to find the respective column in the big dataframe, so we get the sediment at the user-selected location for all times
 --> position_1 = df_big[idx]
 
 ---> similarly, a second position specified by the user can be queried as above: position_2 = df_big[idx2]
 
# 3. Aggregation and interpolation
after getting the sediment values for the respective position, ordered by the dates, some dates have missing values, NaNs, decide to aggregate to the monthly average and then interpolate the ones that are still missing (not so many missing values anymore after monthly aggregation)

# 4. Time series
plot the time series (for a single position, or for multiple positions) for comparison of sediment over time, and over space

# Note 
since the memory of local desktop is not big enough to store all positions' information, 2 positions were selected in advanced and the data were downloaded locally for analysis/plotting
