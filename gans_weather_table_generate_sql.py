import sqlalchemy
import pymysql
import pandas as pd
import functions_for_gans_weather as gw
import sql_credentials as sq

cities = pd.read_sql('cities', con = sq.con)

weather = gw.get_tomorrow_weather_forecast(cities)

weather.to_sql('weather',
               if_exists = 'append',
               con = sq.con,
               index = False)
