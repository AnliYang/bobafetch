""""""


# REFACTOR TO USE YELP PYTHON LIBRARY DOOIIII

import os
import oauth2
import urllib
import urllib2
import json

CONSUMER_KEY = os.environ['YELP_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['YELP_CONSUMER_SECRET']
TOKEN = os.environ['YELP_TOKEN']
TOKEN_SECRET = os.environ['YELP_TOKEN_SECRET']

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'boba'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 1
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# FIXME
def get_radius(time_available, running_speed):
    """Prepares radius for use in request"""

    # takes in time available, and running speed

    # hardcode eating/buying to be like 10 or 15 minutes
    consumption_time = 10

    # radius = 90% of ((time available - eating time) * running speed/60)/2
    radius_miles = .9 * ((time_available - consumption_time) * running_speed/60) / 2

    radius_meters = radius_miles * 1609.34
    # radius needs to go into the request now
    return radius_meters


def request_restaurants(user_address, user_latitude, user_longitude, radius=40000):
    """Prepares OAuth authentication and sends the request to the API."""

    # FIXME: should break out parameter if/else into its own function
    if user_address != "":
        url_params = {
            'location': user_address,
            'limit': 1,
            # Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated.
            'sort': 1,
            'category_filter': 'bubbletea',
            # Search radius in meters. Max value is 40000 meters (25 miles).
            'radius_filter': radius
        }
    else:
        user_lat_lng = str(user_latitude) + ',' + str(user_longitude)

        print "user_lat_lng"
        print user_lat_lng
        print type(user_lat_lng)
        print "*" * 10

        url_params = {
            'll': user_lat_lng,
            'limit': 1,
            # Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated.
            'sort': 1,
            'category_filter': 'bubbletea',
            # Search radius in meters. Max value is 40000 meters (25 miles).
            'radius_filter': radius
        }

        print url_params
        print url_params['ll']
        print type(url_params['ll'])
        print url_params['radius_filter']
        print type(url_params['radius_filter'])
        print "*" * 10



    url = 'https://{0}{1}?'.format(API_HOST, urllib.quote(SEARCH_PATH.encode('utf8')))
    print url
    print "*" * 10

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

    # creates a token object
    token = oauth2.Token(TOKEN, TOKEN_SECRET)

    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)
    # adds more entries to the request dictionary (of parameters for the query, looks like)

    print "oauth request"
    print oauth_request
    print "*" * 10

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    # hashes sensitive parts of the request
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    # generates the final url
    signed_url = oauth_request.to_url()

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
        # response = conn.read()
    finally:
        conn.close()

    print response
    return response


def search(user_address, user_latitude, user_longitude, time_available, running_speed):
    """Query Yelp's Search API"""

    # preps the search params for request()
    # yelp example also passes in the API_HOST and SEARCH_PATH

    # pass

# FIXME:
    # takes in user_address, time available, and running speed
    radius = get_radius(time_available, running_speed)
    response = request_restaurants(user_address, user_latitude, user_longitude, radius)

    return response


if __name__ == "__main__":
    request()
