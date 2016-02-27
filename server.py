"""BobaFetch: Running for bubble tea!"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

import json

import yelp_call

from model import connect_to_db, db, User, Restaurant, Favorite_Restaurant, Visited_Restaurant

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


@app.route('/search', methods=["POST"])
def search():
    '''Searches for restaurant and running route results.'''

    # send requests to the Yelp API
    # parse results from the Yelp API
    # pass results to template and Google Maps API
    # yelp_string = open('scratch/scratch.json').read()
    # yelp_dict = json.loads(yelp_string)

    user_address = request.form.get("address")

    user_latitude = request.form.get("latitude")
    user_longitude = request.form.get("longitude")

    # FIXME: get the other inputs from the form: time available and running speed
    time_available = request.form.get("time-available")
    time_available = int(time_available)

    running_speed = request.form.get("running-speed")
    running_speed = int(running_speed)

    # yelp_dict = yelp_call.request_restaurants(user_address)
    yelp_dict = yelp_call.search(user_address, user_latitude, user_longitude, time_available, running_speed)

    if yelp_dict['total'] > 0:
        index_alias = yelp_dict['businesses'][0]

        name = index_alias['name']
        # note: this address is in the form of a list.
        # this is the form currently being used by the results page
        display_address = index_alias['location']['display_address']
        # note: this set of address info is broken out by line.
        # adding these variables into to use for STORING the adddress in db
        street_address = index_alias['location']['address']
        city = index_alias['location']['city']
        state = index_alias['location']['state_code']
        zip5 = index_alias['location']['postal_code']

        coordinates = index_alias['location']['coordinate']
        yelp_url = index_alias['url']
        image = index_alias['image_url']
        mobile_url = index_alias['mobile_url']
        rating = index_alias['rating']
        rating_img_url = index_alias['rating_img_url']
        review_count = index_alias['review_count']
        yelp_id = index_alias['id']

        return render_template('results.html', name=name,
                                               address=display_address,
                                               yelp_url=yelp_url,
                                               rating=rating,
                                               rating_img_url=rating_img_url,
                                               review_count=review_count,
                                               image=image,
                                               coordinates=coordinates,
                                               user_address=user_address,
                                               user_latitude=user_latitude,
                                               user_longitude=user_longitude,
                                               yelp_id=yelp_id)
    else:
        return render_template('no_results.html')

# got this from Ratings, but unclear why I need to specify the GET method for the form route?
@app.route('/signup', methods=['GET'])
def signup_form():
    '''Show signup (user account creation) form.'''

    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup_process():
    '''Process signup form'''

    # turn the form fields into variables for use
    # instantiate a new user
    # add the user to the db
    # commit to db
    # add a flash message
    # return a redirect...

    # FIXME: Add handling for already existing user

    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]

    new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    # return new user to landing page in logged in state
    session["user_id"] = new_user.user_id

    flash("User %s added." % email)
    flash("Logged in")

    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter(email==email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")

    return redirect("/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


# route for showing multiple results


# route after someone clicks "Map it" to show directions to a particular restaurant


# route for profile page (when someone clicks Profile in header)
@app.route('/profile')
def show_profile():
    """User profile page"""

    return render_template("profile.html")


@app.route("/add-to-favorites", methods=["POST"])
def add_to_favorites():
    """Add a favorite restaurant for a user"""

    yelp_location_id = request.form.get("yelp_id")
    # get the user id from the session?

    # use the yelp_location_id to get the restaurant_id from the db
    # create a new favorites entry for that user-restaurant combo

    # send back success and an id to update the page to indicate action completed
    return jsonify(status="success", id=yelp_id)

@app.route("/add-to-visited", methods=["POST"])
def add_to_visited():
    """Add a visited restaurant for a user"""

    yelp_location_id = request.form.get("yelp_id")
    # get the user id from the session?

    # use the yelp_location_id to get the restaurant_id from the db
    # create a new visited_restaurants entry for that user-restaurant combo

    # send back success and an id to update the page to indicate action completed
    return jsonify(status="success", id=yelp_id)


# route for user's list of favorite restaurants


# route for user's list of trips/routes (visited restaurants)


# kept getting error (below) when trying this from yelp_call, so moving here
# "RuntimeError: application not registered on db instance and no application 
# bound to current context"
def get_restaurants_from_db(list_of_yelp_ids):
    """Grab restaurants from DB, returns a list of restaurant dictionaries."""

    # function for use in displaying search results and for future user favorites page
    # ? jsonify necessary before passing to Jinja template?

    restaurants = []

    for id in list_of_yelp_ids:
        restaurant = {}

        restaurant['name'] = db.session.query(Restaurant.name).filter(Restaurant.yelp_location_id==id).first()
        restaurant['street_address'] = db.session.query(Restaurant.street_address).filter(Restaurant.yelp_location_id==id).first()
        print "*" * 50
        print "street address type coming out of the db:"
        print type(restaurant['street_address'])
        # restaurant['city'] = db.session.query(Restaurant.city).filter(Restaurant.yelp_location_id==id).first()
        # restaurant['state'] = db.session.query(Restaurant.state).filter(Restaurant.yelp_location_id==id).first()
        # restaurant['zip5'] = db.session.query(Restaurant.zip5).filter(Restaurant.yelp_location_id==id).first()
        # restaurant['yelp_url'] = db.session.query(Restaurant.yelp_url).filter(Restaurant.yelp_location_id==id).first()
        # restaurant['rating'] = db.session.query(Restaurant.rating).filter(Restaurant.yelp_location_id==id).first()
        # restaurant['rating_img_url'] = db.session.query(Restaurant.rating_img_url).filter(Restaurant.yelp_location_id==id).first()
        # restaurant['yelp_id'] = id

        # latitude = db.session.query(Restaurant.latitude).filter(Restaurant.yelp_location_id==id).first()
        # longitude = db.session.query(Restaurant.longitude).filter(Restaurant.yelp_location_id==id).first()
        # restaurant[coordinates] =

        restaurants.append(restaurant)

    return restaurants

if __name__ == "__main__":
# using the Flask Debug bar, including setting debug = True
    app.debug = True
    DebugToolbarExtension(app)

    from model import connect_to_db, db
    connect_to_db(app)
    db.create_all()

    app.run()
