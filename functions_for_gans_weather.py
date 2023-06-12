import pandas as pd
import requests
import datetime
import API_keys as keys

def get_tomorrow_weather_forecast(cities):
    """Finds tomorrow's weather information using latitude and longitude columns in a pandas Dataframe. 
    Returns a dataframe with columns for date-time, temperature (C), windspeed, and weather description."""
    out_df = pd.DataFrame({
    'city_id': [],
    'date_time': [],
    'temp': [],
    'wind_speed': [],
    'outlook': []
    })
    tomorrow = datetime.datetime.now().date() + datetime.timedelta(days=1)
    for _, row in cities.iterrows():
        lat = row.lat
        lon = row.lon
        parameters = {
            'lat': lat,
            'lon': lon,
            'appid': keys.OpenWeather_key,
            'units': 'metric'
        }
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast',
            params = parameters)
        response.raise_for_status() # raises an error if the status code is not 200
        results = response.json()['list']
        for result in results:

            result['weather'] = result['weather'][0]
            df_int = pd.json_normalize(result)
            df_int['city_id'] = row.city_id
            df_int = df_int[['city_id', 'dt_txt', 'main.temp', 'wind.speed', 'weather.description']]
            df_int.columns = out_df.columns
            out_df = pd.concat([out_df, df_int])
    out_df['date_time'] = pd.to_datetime(out_df['date_time'])
    out_df = out_df.loc[out_df.date_time.dt.date == tomorrow]
    return out_df