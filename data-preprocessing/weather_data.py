from wwo_hist import retrieve_hist_data
import pandas as pd


'''

http://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&cnt={cnt}&appid={YOUR_API_KEY}

Parameters:
lat, lon coordinates of the location of your interest

type type of the call, keep this parameter in the API call as 'hour'

start start date (unix time, UTC time zone), e.g. start=1369728000

end end date (unix time, UTC time zone), e.g. end=1369789200

cnt amount of returned data (one per hour, can be used instead of 'end')

Examples of API calls:
http://history.openweathermap.org/data/2.5/history/city?lat=41.85&lon=-87.65&appid={YOUR_API_KEY}
'''

YOUR_API_KEY = "xxxxxxx"

frequency= 24  # get daily data, each 24 hours
start_date = '11-Jan-2020'
end_date = '11-MAR-2020'
api_key = 'e1634399315c4ec0b67203402202304'
location_list = ['golfito']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)



df = pd.read_csv('golfito.csv') # data downloaded is named as the city
