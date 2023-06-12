import pandas as pd
import requests
from bs4 import BeautifulSoup
import pycountry

def scrape_wikipedia_for_city_info(cities_list):
    """Accesses wikipedia pages of cities, given a list of cities.
    returns a list of soups ready for data extraction with BeautifulSoup."""
    # Get responses from wikipedia and make sure they're all ok
    urls = ['https://en.wikipedia.org/wiki/' + city.replace(' ', '_') for city in cities_list]
    headers = {'Accept-Language': 'en-US,en;q=0.8'}
    responses = [requests.get(url, headers = headers) for url in urls]
    status_codes = [response.status_code for response in responses]
    for response in responses:
        response.raise_for_status()
    soups = [BeautifulSoup(response.content, 'html.parser') for response in responses]
    return soups

def get_city_name(soups):
    """Extracts the city names from the Wikipedia soups created by scrape_wikipedia_for_city_info()."""
    names = [soup.select_one('#firstHeading').get_text() for soup in soups]
    return pd.Series(names, name = 'city_name')

def make_city_id(soups):
    """Creates a unique identifier for each city"""
    names = get_city_name(soups)
    city_ids = names.str[0:3] + names.index.to_series().astype('str')
    return pd.Series(city_ids, name = 'city_id')
    
def get_city_country_code(soups):
    """Gets the two-letter country code for each city's country.
    Relies on the name of the country in the Wikipedia soup and the pycountry library."""
    countries = [soup.select_one('.infobox-label:-soup-contains("Country")').parent.select_one('td.infobox-data').get_text().strip() for soup in soups]
    country_codes = [pycountry.countries.get(name = country).alpha_2 for country in countries]
    return pd.Series(country_codes, name = 'country_code')

def get_city_coords(soups):
    """Gets coordinates for each city in decimal degrees from GeoHack."""
    geohack_urls = ["https:"+soup.select_one('.infobox-full-data:-soup-contains("Coordinates")').a['href'] for soup in soups]
    headers = {'Accept-Language': 'en-US,en;q=0.8'}
    geohack_responses = [requests.get(geohack_url, headers = headers) for geohack_url in geohack_urls]
    for geohack_response in geohack_responses:
        geohack_response.raise_for_status()
    g_soups = [BeautifulSoup(response.content, 'html.parser') for response in geohack_responses]
    lats = [float(g_soup.select_one('.p-latitude').get_text()) for g_soup in g_soups]
    lons = [float(g_soup.select_one('.p-longitude').get_text()) for g_soup in g_soups]
    return pd.DataFrame({'lat': lats, 'lon': lons})

def combine_city_info_to_df(city_ids, names, country_codes, coords):
    """Combines the output of all of the above functions into a single data frame."""
    df = pd.concat([city_ids, names, country_codes, coords], axis = 1)
    return df

def generate_cities_df_from_list_of_names(cities):
    """Wrapper function that takes a list of city names and returns a dataframe with with data scraped from Wikipedia."""
    soups = scrape_wikipedia_for_city_info(cities)
    return combine_city_info_to_df(
        city_ids = make_city_id(soups),
        names = get_city_name(soups),
        country_codes = get_city_country_code(soups),
        coords = get_city_coords(soups)
    )

