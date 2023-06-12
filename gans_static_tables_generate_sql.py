import sqlalchemy
import pymysql
import functions_for_gans_cities as gc
import functions_for_gans_airports as ga
import sql_credentials as sq

cities = ['Freiburg im Breisgau', 'Ann Arbor, Michigan', 'Winters, California', 'Sofia', 'Berkeley, California', 'San Francisco, California', 'Saint Paul, Minnesota']
cities = gc.generate_cities_df_from_list_of_names(cities)
cities.to_sql('cities',
              if_exists = 'append',
              con = sq.con,
              index = False)

results = ga.get_api_results_for_airports_near_cities(cities)
airports = ga.make_airports_table(results)
airports.to_sql('airports',
                if_exists = 'append',
                con = sq.con,
                index = False)

airports_cities = ga.make_airports_cities_table(cities, results)
airports_cities.to_sql('airports_cities',
                       if_exists = 'append',
                       con = sq.con,
                       index = False)