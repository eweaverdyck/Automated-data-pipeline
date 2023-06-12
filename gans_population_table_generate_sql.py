import sqlalchemy
import pymysql
import pandas as pd
import functions_for_gans_population as gp
import sql_credentials as sq

cities = pd.read_sql('cities', con = sq.con)

populations = gp.make_populations_table(cities)

populations.to_sql('populations',
               if_exists = 'append',
               con = sq.con,
               index = False)

