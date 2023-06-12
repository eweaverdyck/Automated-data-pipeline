import pandas as pd
import requests
import API_keys as keys


def get_api_results_for_airports_near_cities(cities):
    """Calls the AeroDataBox airports API to get all airports within 50 km of each city in a dataframe.
    Assumes cities data frame has columns 'lat' and 'lon' with coordinates in decimal degrees.
    Returns a list containing, for each city, a list of airports represented as dictionaries."""
    results = []
    for i in range(cities.shape[0]):
        url = "https://aerodatabox.p.rapidapi.com/airports/search/location"

        querystring = {"lat":cities['lat'][i],"lon":cities['lon'][i],"radiusKm":"50","limit":"10","withFlightInfoOnly":"true"}

        headers = {
        "X-RapidAPI-Key": keys.ADB_key,
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        results.append(response.json()['items'])

    return results

def make_airports_cities_table(cities, results):
    """Converts output of get_api_results_for_airports_near_cities() to a dataframe of airport - city pairs"""
    airport_results_df = pd.Series(results, name = 'airport_results', index = cities.city_id).reset_index()
    city_airports_dict = {'city_id': [], 'airport_icao': []}
    for _, city_airports in airport_results_df.iterrows():
        city = city_airports.city_id
        for airport in city_airports.airport_results:
            airport_icao = airport.get('icao', None)
            city_airports_dict['city_id'].append(city)
            city_airports_dict['airport_icao'].append(airport_icao)
    return pd.DataFrame(city_airports_dict)
    
def make_airports_table(results):
    """Converts output of get_api_results_for_airports_near_cities() to a dataframe of airports"""
    airports_dict = {
    'airport_icao': [],
    'airport_name': []
    }
    for city_airports in results:
        for airport in city_airports:
            airports_dict['airport_icao'].append(airport.get('icao', None))
            airports_dict['airport_name'].append(airport.get('name', None))
    return pd.DataFrame(airports_dict).drop_duplicates()