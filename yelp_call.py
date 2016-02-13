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


def request(user_address):
    """Prepares OAuth authentication and sends the request to the API."""

    # FIXME: hardcoded for now, and in here instead of request
    url_params = {
        'location': user_address,
        'limit': 1,
        'sort': 1,
        'category_filter': 'bubbletea'
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

    print response
    return response


def search():
    """Query Yelp's Search API"""

    # preps the search params for request()
    # yelp example also passes in the API_HOST and SEARCH_PATH

    pass


if __name__ == "__main__":
    request()
