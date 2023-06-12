import requests
import pandas as pd
import datetime
import API_keys as keys

def reverse_geocode_geonames(city):
    """Gets GeoNames data about the city (population > 1000) closest to the coordinates of a city from the cities data frame."""
    url = 'http://api.geonames.org/findNearbyPlaceNameJSON'
    params = {
        'lat': city.lat,
        'lng': city.lon,
        'username': keys.GeoNames_key,
        'cities': 'cities1000'
    }
    response = requests.get(
        url = url,
        params = params
    )
    return response.json()

def make_populations_table(cities):
    """Uses reverse_geocode_geonames() to create a data frame of city populations given a cities data frame."""
    population = []
    city_ids = []
    pop_year = []
    for _, city in cities.iterrows():
        population.append(reverse_geocode_geonames(city)['geonames'][0]['population'])
        city_ids.append(city.city_id)
        pop_year.append(datetime.datetime.now())
    populations_df = pd.DataFrame({
        'city_id': city_ids,
        'population': population,
        'pop_year': pop_year
    })
    return populations_df