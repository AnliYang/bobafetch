""""""


# REFACTOR TO USE YELP PYTHON LIBRARY DOOIIII

import os
import oauth2
import urllib
import urllib2
import json
from model import db, User, Restaurant, Favorite_Restaurant, Visited_Restaurant

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


def request_restaurants(user_address, user_latitude, user_longitude, radius=40000, limit=10):
    """Prepares OAuth authentication and sends the request to the API."""

    # FIXME: should break out parameter if/else into its own function
    if user_address != "":
        url_params = {
            'location': user_address,
            'limit': limit,
            # Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated.
            'sort': 1,
            'category_filter': 'bubbletea',
            # Search radius in meters. Max value is 40000 meters (25 miles).
            'radius_filter': radius
        }
    else:
        user_lat_lng = user_latitude + ',' + user_longitude

        url_params = {
            'll': user_lat_lng,
            'limit': limit,
            # Sort mode: 0=Best matched (default), 1=Distance, 2=Highest Rated.
            'sort': 1,
            'category_filter': 'bubbletea',
            # Search radius in meters. Max value is 40000 meters (25 miles).
            'radius_filter': radius
        }

    url = 'https://{0}{1}?'.format(API_HOST, urllib.quote(SEARCH_PATH.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

    # creates a token object
    token = oauth2.Token(TOKEN, TOKEN_SECRET)

    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)
    # adds more entries to the request dictionary (of parameters for the query, looks like)

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

    yelp_location_ids = save_restaurants(response)

    # should return a list of the yelp_location_ids, which is the primary key for restaurants table
    # return response
    return yelp_location_ids


def save_restaurants(response):
    """Takes in response dictionary, saves restaurants to the DB."""

    # FIXME: will need to account for duplicates: if a restaurant is already in 
    # the db (match on yelp id), you'll need to update the existing entry rather
    # than creating a new one (probably an if statement first)
    yelp_location_ids = []

    for i in range(len(response['businesses'])):
        # pull the items out of the response for a given restaurant
        index_alias = response['businesses'][i]

        name = index_alias['name']
        display_address = index_alias['location']['display_address']

        # print "*" * 50
        # print "type for street address going into the db"
        # print type(display_address)

        # city = index_alias['location']['city']
        # state = index_alias['location']['state_code']
        # zip5 = index_alias['location']['postal_code']
        coordinates = index_alias['location']['coordinate']
        yelp_url = index_alias['url']
        image_url = index_alias['image_url']
        mobile_url = index_alias['mobile_url']
        rating = index_alias['rating']
        rating_img_url = index_alias['rating_img_url']
        review_count = index_alias['review_count']
        
        yelp_location_id = index_alias['id']
        yelp_location_ids.append(yelp_location_id)

        existing_restaurant = db.session.query(Restaurant).filter(Restaurant.yelp_location_id==yelp_location_id).all()

        if existing_restaurant:
            # print existing_restaurant
            # print len(existing_restaurant)
            # print existing_restaurant[0].yelp_location_id
            print "it's totally already in there."
            # FIXME would ideally update with new restaurant location

        else:
            # instantiate the Restaurant object
            new_restaurant = Restaurant(yelp_location_id=yelp_location_id,
                                        name=name,
                                        display_address=display_address,
                                        # city=city,
                                        # state=state,
                                        # zip5=zip5,
                                        latitude=coordinates['latitude'],
                                        longitude=coordinates['longitude'],
                                        yelp_url=yelp_url,
                                        image_url=image_url,
                                        mobile_url=mobile_url,
                                        rating=rating,
                                        rating_img_url=rating_img_url,
                                        review_count=review_count)

            # add to the db and commit!
            db.session.add(new_restaurant)
            db.session.commit()

    return yelp_location_ids


def convert_response():
    """Turn the Yelp response into a list of dictionaries"""

    pass
    # only necessary/useful if you're not saving to the dictionary right now


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
