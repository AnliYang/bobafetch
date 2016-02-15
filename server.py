"""BobaFetch: Running for bubble tea!"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request
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

    user_address = request.form.get("Address")

    yelp_dict = yelp_call.request(user_address)

    index_alias = yelp_dict['businesses'][0]
    # note: this address is in the form of a list.
    name = index_alias['name']
    address = index_alias['location']['display_address']
    coordinates = index_alias['location']['coordinate']
    yelp_url = index_alias['url']
    image = index_alias['image_url']
    mobile_url = index_alias['mobile_url']
    rating = index_alias['rating']
    rating_img_url = index_alias['rating_img_url']
    review_count = index_alias['review_count']

    # send requests to the Maps, Directions, etc. APIs

    # parse results from Google Maps APIs, pass to template

    # return redirect('/result')
    return render_template('results.html', name=name,
                                           address=address,
                                           yelp_url=yelp_url,
                                           rating=rating,
                                           rating_img_url=rating_img_url,
                                           review_count=review_count,
                                           image=image,
                                           coordinates=coordinates)


@app.route('/result')
def result():
    '''Shows result(s) page with restaurant and running route information.'''

    pass

if __name__ == "__main__":
# using the Flask Debug bar, including setting debug = True
    app.debug = True
    DebugToolbarExtension(app)

    app.run()
