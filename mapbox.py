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

    if response.get('features'):
        longitude, latitude = response['features'][0]['center']
        return (latitude, longitude)


def reverse_geocode(latitude, longitude):
    """Given lat/long pair, return an address."""

    url = GEOCODE_BASE_URL + str(longitude) + ',' + str(latitude) + '.json'
    params = {
        'access_token': ACCESS_TOKEN
    }

    response = requests.get(url, params=params).json()

    if response.get('features'):
        return response['features'][0]['place_name']
