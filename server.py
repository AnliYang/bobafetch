"""BobaFetch: Running for bubble tea!"""

import jinja2 as jinja

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import json

import yelp_call

from model import connect_to_db, db, User, Restaurant, Favorite_Restaurant, Visited_Restaurant

app = Flask(__name__)

# To use the Flask sessions and the debug toolbar
app.secret_key = "ALLOFTHEBOBAAREMINE"

# Letting Jinja help me by raising an error upon use of an
# undefined variable, as opposed to letting it fail silently on me
app.jinja_env.undefined = jinja.StrictUndefined


@app.route('/')
def index():
    '''Homepage'''

    return render_template('landing.html')


@app.route('/oldlanding')
def alt_landing():
    '''Alternate homepage'''

    return render_template("old_landing.html")


@app.route('/signup', methods=['GET'])
def signup_form():
    '''Show signup (user account creation) form.'''

    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup_process():
    """Process signup form"""

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

    user = User.query.filter(User.email==email).first()

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
@app.route('/results', methods=['POST'])
def show_results():
    """Shows restaurant search results."""

    # make the yelp call, get the list of restaurant_ids back
    # use the list of restaurants to make call to DB, get list of dictionaries back
    # jsonify the list of dictionaries to send to the results page

    user_address = request.form.get("address")

    user_latitude = request.form.get("latitude")
    user_longitude = request.form.get("longitude")

    time_available = request.form.get("time-available")
    time_available = int(time_available)

    running_speed = request.form.get("running-speed")
    running_speed = int(running_speed)

    yelp_location_ids = yelp_call.search(user_address, user_latitude, user_longitude, time_available, running_speed)
    restaurants = get_restaurants_from_db(yelp_location_ids)

    if restaurants:
        return render_template('results.html', restaurants=restaurants,
                                               # restaurants_range=restaurants_range,
                                               user_address=user_address,
                                               user_latitude=user_latitude,
                                               user_longitude=user_longitude,
                                               running_speed=running_speed)

    else:
        # return render_template('no_results.html')
        flash("Sorry, it appears there's no boba near you!")
        return redirect("/")


# route after someone clicks "Map it" to show directions to a particular restaurant
@app.route('/map', methods=["POST"])
def show_map():
    """Shows map route to individual restaurant."""

    # user_address, user_latitude, user_longitude, coordinates['latitude'], coordinates['longitude']
    yelp_location_id = request.form.get("yelp-id")
    user_address = request.form.get("user-address")
    user_latitude = request.form.get("user-lat")
    user_longitude = request.form.get("user-lng")
    running_speed = request.form.get("run-speed")

    restaurant = db.session.query(Restaurant).filter(Restaurant.yelp_location_id==yelp_location_id).one()
    # restaurant_latitude = restaurant.latitude
    # restaurant_longitude = restaurant.longitude

    return render_template("map.html", user_address=user_address,
                                       user_latitude=user_latitude,
                                       user_longitude=user_longitude,
                                       restaurant=restaurant,
                                       running_speed=running_speed)


# route for profile page (when someone clicks Profile in header)
@app.route('/profile')
def show_profile():
    """User profile page"""

    user_id = session["user_id"]

    user = db.session.query(User).filter(User.user_id==user_id).one()

    return render_template("profile.html", user=user)


@app.route("/add-to-favorites", methods=["POST"])
def add_to_favorites():
    """Add a favorite restaurant for a user"""

    yelp_location_id = request.form.get("yelp-id")
    user_id = session["user_id"]

    # create a new favorites entry for that user-restaurant combo
    new_favorite = Favorite_Restaurant(user_id=user_id,
                                       yelp_location_id=yelp_location_id)

    db.session.add(new_favorite)
    db.session.commit()

    # send back success and an id to update the page to indicate action completed
    return jsonify(status="success", id=yelp_location_id)

@app.route("/add-to-visited", methods=["POST"])
def add_to_visited():
    """Add a visited restaurant for a user"""

    yelp_location_id = request.form.get("yelp-id")
    user_id = session["user_id"]

    new_visit = Visited_Restaurant(user_id=user_id,
                                       yelp_location_id=yelp_location_id)

    db.session.add(new_visit)
    db.session.commit()

    return jsonify(status="success", id=yelp_location_id)


@app.route("/check-for-favorite", methods=["POST"])
def check_for_favorite():
    """Check for a favorite restaurant for a user"""

    print "CHECKING FOR FAVORITES NOWWWWWW"

    yelp_location_id = request.form.get("yelp-id")
    user_id = session["user_id"]

    print "yelp_location_id =", yelp_location_id
    print "user_id =", user_id

    favorite = db.session.query(Favorite_Restaurant).filter(Favorite_Restaurant.yelp_location_id==yelp_location_id,
                                                            Favorite_Restaurant.user_id==user_id).all()

    print "favorite = ", favorite

    if favorite:
    # send back success and an id to update the page to indicate action completed
        return jsonify(status="success", id=yelp_location_id)

    else:
        return jsonify(status="")


@app.route("/checkForVisited", methods=["POST"])
def check_for_visited():
    """Check for a visited restaurant for a user"""

    print "CHECKING FOR Visited NOWWWWWW"

    yelp_location_id = request.form.get("yelp-id")
    user_id = session["user_id"]

    print "yelp_location_id =", yelp_location_id
    print "user_id =", user_id

    visited = db.session.query(Visited_Restaurant).filter(Visited_Restaurant.yelp_location_id==yelp_location_id,
                                                            Visited_Restaurant.user_id==user_id).all()

    print "visited = ", visited

    if visited:
    # send back success and an id to update the page to indicate action completed
        return jsonify(status="success", id=yelp_location_id)

    else:
        return ""

# route for user's list of favorite restaurants
@app.route("/favorite-restaurants")
def display_favorites():
    """Displays page of favorite restaurants."""

    # grab user_id from session
    user_id = session["user_id"]

    # query the database for that user's favorites
    favorites = db.session.query(Favorite_Restaurant.yelp_location_id).filter(Favorite_Restaurant.user_id==user_id).all()
    # add the restaurant objects to a list
    print "favorites: ", favorites

    # generate a list of restaurants
    restaurants = get_restaurants_from_db(favorites)
    print "restaurants: ", restaurants

    # send the list to a favorites page template

    return render_template("favorites.html", restaurants=restaurants)


# route for user's list of trips/routes (visited restaurants)
@app.route("/visited-restaurants")
def display_visited():
    """Displays page of visited restaurants."""

    user_id = session["user_id"]

    visited_restaurants = db.session.query(Visited_Restaurant.yelp_location_id).filter(Visited_Restaurant.user_id==user_id).all()

    restaurants = get_restaurants_from_db(visited_restaurants)

    return render_template("visited.html", restaurants=restaurants)

@app.route("/about")
def display_about():
    return render_template("about.html")

def get_restaurants_from_db(list_of_yelp_ids):
    """Grab restaurants from DB, returns a list of restaurant dictionaries."""

    restaurants = []

    for id in list_of_yelp_ids:
        restaurant = db.session.query(Restaurant).filter(Restaurant.yelp_location_id==id).one()
        restaurants.append(restaurant)

    return restaurants

if __name__ == "__main__":
# using the Flask Debug bar, including setting debug = True
    # app.debug = True
    # DebugToolbarExtension(app)

    from model import connect_to_db, db
    connect_to_db(app)
    db.create_all()

    app.run()
