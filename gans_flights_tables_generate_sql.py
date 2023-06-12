import sqlalchemy
import pymysql
import functions_for_gans_flights as gf
import pandas as pd
import sql_credentials as sq

airports_queried = pd.read_sql('airports', con = sq.con)

flights = gf.get_tomorrows_flights(airports_queried)


flights.to_sql('flights',
               if_exists = 'append',
               con = sq.con,
               index = False)