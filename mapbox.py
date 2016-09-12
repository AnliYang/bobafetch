"""Calls related to the Mapbox API"""

import os, requests

ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
GEOCODE_BASE_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

def geocode(address):
    """Given an address, return the lat/long."""

    url = GEOCODE_BASE_URL + address + '.json'
    params = {
        'access_token': ACCESS_TOKEN
    }

    response = requests.get(url, params=params).json()
    longitude, latitude = response['features'][0]['center']

    return (latitude, longitude)


def reverse_geocode(latitude, longitude):
    """Given lat/long pair, return an address."""

    url = GEOCODE_BASE_URL + str(longitude) + ',' + str(latitude) + '.json'
    params = {
        'access_token': ACCESS_TOKEN
    }

    response = requests.get(url, params=params).json()

    return response['features'][0]['place_name']



# curl -X GET "https://api.mapbox.com/geocoding/v5/mapbox.places/1617-hess-rd-redwood-city-ca-94061.json?country=us&access_token=pk.eyJ1IjoiYW5saXlhbmciLCJhIjoiY2lvZ25wbTB4MDFrdHU3a212eGZwcW91NSJ9.GOtW72gefCHdD1Y-6bza-w"
