"""Calls related to the Yelp API."""

import os, urllib, urllib2, json
from furl import furl
from model import db, User, Restaurant, Favorite_Restaurant, Visited_Restaurant

API_KEY = os.environ['YELP_API_KEY']
API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'boba'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 1
BUSINESS_SEARCH_PATH = '/v3/businesses/search'
MAX_RADIUS = 40000

def get_radius(time_available, running_speed):
    """Prepares radius for use in request. Integer required by Yelp API."""

    # hardcode extra time for eating/buying
    consumption_time = 10

    # rounded down because working with radius instead of route distance
    radius_miles = .9 * ((time_available - consumption_time) * running_speed/60) / 2
    radius_meters = radius_miles * 1609.34

    return min(int(radius_meters), MAX_RADIUS)

def request_restaurants(user_latitude, user_longitude, radius=40000, limit=20):
    """Requests restaurants from Yelp API."""

    url_params = {
        'latitude': user_latitude,
        'longitude': user_longitude,
        'limit': limit,
        'sort_by': 'distance',
        'categories': 'bubbletea',
        # Search radius in meters. Max value is 40000 meters (25 miles).
        'radius': radius
    }

    url = furl('https://{0}{1}?'.format(API_HOST, urllib.quote(BUSINESS_SEARCH_PATH.encode('utf8')))).set(url_params).url
    auth_header = 'Bearer {0}'.format(API_KEY)

    req = urllib2.Request(url)
    req.add_header('Authorization', auth_header)
    resp = urllib2.urlopen(req)
    content = json.loads(resp.read())

    yelp_location_ids = save_restaurants(content)

    return yelp_location_ids


def save_restaurants(response):
    """Takes in response dictionary, saves restaurants to the DB."""
    yelp_location_ids = []

    for i in range(len(response['businesses'])):
        index_alias = response['businesses'][i]
        name = index_alias['name']
        street1 = index_alias['location']['display_address'][0].split('"')[0]
        city = index_alias['location']['city']
        state = index_alias['location']['state']
        zip5 = index_alias['location']['zip_code']
        coordinates = index_alias['coordinates']
        yelp_url = index_alias['url']
        image_url = index_alias['image_url']
        rating = index_alias['rating']
        review_count = index_alias['review_count']
        yelp_location_id = index_alias['id']

        yelp_location_ids.append(yelp_location_id)

        existing_restaurant = db.session.query(Restaurant).filter(Restaurant.yelp_location_id==yelp_location_id).all()

        if existing_restaurant:
            pass #FIXME: update existing entry

        else:
            new_restaurant = Restaurant(yelp_location_id=yelp_location_id,
                                        name=name,
                                        # display_address=display_address,
                                        street1=street1,
                                        # street2=street2,
                                        city=city,
                                        state=state,
                                        zip5=zip5,
                                        latitude=coordinates['latitude'],
                                        longitude=coordinates['longitude'],
                                        yelp_url=yelp_url,
                                        image_url=image_url,
                                        rating=rating,
                                        review_count=review_count)
            db.session.add(new_restaurant)
            db.session.commit()

    return yelp_location_ids


def search(user_latitude, user_longitude, time_available, running_speed):
    """Query Yelp's Search API"""

    radius = get_radius(time_available, running_speed)
    response = request_restaurants(user_latitude, user_longitude, radius)

    return response


if __name__ == "__main__":
    pass
