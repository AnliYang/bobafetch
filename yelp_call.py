"""Calls related to the Yelp API."""

import os, oauth2, urllib, urllib2, json
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

def get_radius(time_available, running_speed):
    """Prepares radius for use in request"""

    # hardcode extra time for eating/buying
    consumption_time = 10

    # rounded down because working with radius instead of route distance
    radius_miles = .9 * ((time_available - consumption_time) * running_speed/60) / 2
    radius_meters = radius_miles * 1609.34

    return radius_meters


def request_restaurants(user_latitude, user_longitude, radius=40000, limit=20):
    """Prepares OAuth authentication and sends the request to the API."""

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

    # creates a consumer object
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

    # creates a token object
    token = oauth2.Token(TOKEN, TOKEN_SECRET)

    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)
    # adds more entries to the request dictionary (of parameters for the query, looks like)

    # adds oauth bits to the oauth
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

    # open up a connection to the signed_url
    conn = urllib2.urlopen(signed_url, None)

    try:
        response = json.loads(conn.read())
        # response = conn.read()
    finally:
        conn.close()

    yelp_location_ids = save_restaurants(response)

    return yelp_location_ids


def save_restaurants(response):
    """Takes in response dictionary, saves restaurants to the DB."""

    yelp_location_ids = []

    for i in range(len(response['businesses'])):
        index_alias = response['businesses'][i]
        name = index_alias['name']
        street1 = index_alias['location']['address'][0].split('"')[0]
        city = index_alias['location']['city']
        state = index_alias['location']['state_code']
        zip5 = index_alias['location']['postal_code']
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
                                        mobile_url=mobile_url,
                                        rating=rating,
                                        rating_img_url=rating_img_url,
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
