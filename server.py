"""BobaFetch: Running for bubble tea!"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

import json

import yelp_call

app = Flask(__name__)

# To use the Flask sessions and the debug toolbar
app.secret_key = "ALLOFTHEBOBAAREMINE"

# Letting Jinja help me by raising an error upon use of an
# undefined variable, as opposed to letting it fail silently on me
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    '''Homepage'''

    return render_template('landing.html')


# FIXME: currently only redirects to results page
@app.route('/search', methods=["POST"])
def search():
    '''Searches for restaurant and running route results.'''

    # send requests to the Yelp API
    # parse results from the Yelp API
    # pass results to template and Google Maps API
    # FIXME: currently getting a single result from a static file
    # yelp_string = open('scratch/scratch.json').read()
    # yelp_dict = json.loads(yelp_string)

    yelp_dict = yelp_call.request()

    # note: this address is in the form of a list.
    address = yelp_dict['businesses'][0]['location']['display_address']
    coordinates = yelp_dict['businesses'][0]['location']['coordinate']
    yelp_url = yelp_dict['businesses'][0]['url']
    image = yelp_dict['businesses'][0]['image_url']
    mobile_url = yelp_dict['businesses'][0]['mobile_url']
    rating = yelp_dict['businesses'][0]['rating']
    rating_img_url = yelp_dict['businesses'][0]['rating_img_url']
    review_count = yelp_dict['businesses'][0]['review_count']

    # send requests to the Maps, Directions, etc. APIs

    # parse results from Google Maps APIs, pass to template

    # return redirect('/result')
    return render_template('results.html', address=address,
                                           yelp_url=yelp_url,
                                           rating=rating,
                                           rating_img_url=rating_img_url,
                                           review_count=review_count,
                                           image=image)


@app.route('/result')
def result():
    '''Shows result(s) page with restaurant and running route information.'''

    pass

if __name__ == "__main__":
# using the Flask Debug bar, including setting debug = True
    app.debug = True
    DebugToolbarExtension(app)

    app.run()
