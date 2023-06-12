import pandas as pd
import requests
import datetime
import API_keys as keys

def get_time_ranges():
    """ Create a tuple with two tuples containing the beginning and end time of each range"""
    format = '%Y-%m-%dT%H:%M'
    tomorrow = datetime.datetime.now().replace(hour = 00, minute = 00) + datetime.timedelta(days = 1) 
    start = tomorrow.strftime(format)
    middle = (tomorrow + datetime.timedelta(hours = 12)).strftime(format)
    end = (tomorrow + datetime.timedelta(hours = 24)).strftime(format)
    return((start, middle), (middle, end))

def get_arrival_data(arrival_dict, airport_code):
    """extract relevant information from the dictionary containing all information about each arrival.
    .setdefault() allows the function to return 'unknown' in the case of missing data"""
    return {
        'flight_num': arrival_dict.setdefault('number', ''),
        'arrival_icao': airport_code,
        'departure_icao': arrival_dict
            .setdefault('departure', '')
            .setdefault('airport', '')
            .setdefault('icao', ''),
        'arrival_time': datetime.datetime.strptime(
            arrival_dict
                .setdefault('arrival', '')
                .setdefault('scheduledTimeLocal', '')[:16],
            '%Y-%m-%d %H:%M')
    }

def get_tomorrows_flights(airports_queried):
	"""Given a set of airports, gets arrivals data for 24 hours starting at midnight local time of the date following today's date."""
	all_arrivals = pd.DataFrame({
		'flight_num': [],
		'arrival_icao': [],
		'departure_icao': [],
		'arrival_time': []
	})
	for airport_code in airports_queried.airport_icao:
		for range in get_time_ranges():
			start_time, end_time = range

			url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{airport_code}/{start_time}/{end_time}"

			querystring = {"withLeg":"true","direction":"Arrival","withCancelled":"false","withCodeshared":"false","withCargo":"false","withPrivate":"false","withLocation":"false"}

			headers = {
				"X-RapidAPI-Key": keys.ADB_key,
				"X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
			}

			response = requests.get(url, headers=headers, params=querystring)
			if response.status_code != 200:
				continue
			all_arrivals = pd.concat([all_arrivals, pd.DataFrame(list(map(lambda x: get_arrival_data(x, airport_code), response.json()['arrivals'])))])
	return all_arrivals