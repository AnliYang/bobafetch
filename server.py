"""BobaFetch: Running for bubble tea!"""

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import jinja2 as jinja
import json

import yelp_call

from model import connect_to_db, db, User, Restaurant, Favorite_Restaurant, Visited_Restaurant

app = Flask(__name__)
app.secret_key = "ALLOFTHEBOBAAREMINE"

# Letting Jinja help me by raising an error upon use of an
# undefined variable, as opposed to letting it fail silently on me
app.jinja_env.undefined = jinja.StrictUndefined


@app.route('/')
def index():
    '''Homepage'''

    return render_template('landing.html')


@app.route('/signup', methods=['GET'])
def signup_form():
    '''Show signup (user account creation) form.'''

    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup_process():
    """Process signup form"""
    # FIXME: Add handling for already existing user, put in place security measures

    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]

    new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

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


@app.route('/results', methods=['POST'])
def show_results():
    """Shows restaurant search results."""

    user_address = request.form.get("address")
    user_latitude = request.form.get("latitude")
    user_longitude = request.form.get("longitude")
    time_available = int(request.form.get("time-available"))
    running_speed = int(request.form.get("running-speed"))

    yelp_location_ids = yelp_call.search(user_address, user_latitude, user_longitude, time_available, running_speed)
    restaurants = get_restaurants_from_db(yelp_location_ids)

    if restaurants:
        return render_template('results.html', restaurants=restaurants,
                                               user_address=user_address,
                                               user_latitude=user_latitude,
                                               user_longitude=user_longitude,
                                               running_speed=running_speed)
    else:
        flash("Sorry, it appears there's no boba near you!")
        return redirect("/")


@app.route('/map', methods=["POST"])
def show_map():
    """Shows map route to individual restaurant."""

    yelp_location_id = request.form.get("yelp-id")
    user_address = request.form.get("user-address")
    user_latitude = request.form.get("user-lat")
    user_longitude = request.form.get("user-lng")
    running_speed = request.form.get("run-speed")

    restaurant = db.session.query(Restaurant).filter(Restaurant.yelp_location_id==yelp_location_id).one()

    return render_template("map.html", user_address=user_address,
                                       user_latitude=user_latitude,
                                       user_longitude=user_longitude,
                                       restaurant=restaurant,
                                       running_speed=running_speed)


@app.route("/add-to-favorites", methods=["POST"])
def add_to_favorites():
    """Add a favorite restaurant for a user"""

    yelp_location_id = request.form.get("yelp-id")
    user_id = session.get("user_id")

    if user_id:
        new_favorite = Favorite_Restaurant(user_id=user_id,
                                           yelp_location_id=yelp_location_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify(status="favorite", id=yelp_location_id)

    else:
        return jsonify(status="logged-out-user")

@app.route("/add-to-visited", methods=["POST"])
def add_to_visited():
    """Add a visited restaurant for a user"""

    yelp_location_id = request.form.get("yelp-id")
    user_id = session.get("user_id")

    if user_id:
        new_visit = Visited_Restaurant(user_id=user_id,
                                           yelp_location_id=yelp_location_id)
        db.session.add(new_visit)
        db.session.commit()

        return jsonify(status="visited", id=yelp_location_id)

    else:
        return jsonify(status="logged-out-user")


@app.route("/check-for-favorite", methods=["GET"])
def check_for_favorite():
    """Check for a favorite restaurant for a user"""

    print "got into the favorite-checking function"

    yelp_location_id = request.args.get("yelp-id")
    user_id = session["user_id"]

    favorite = db.session.query(Favorite_Restaurant).filter(Favorite_Restaurant.yelp_location_id==yelp_location_id,
                                                            Favorite_Restaurant.user_id==user_id).all()

    if favorite:
        return jsonify(status="favorite", id=yelp_location_id)

    else:
        return jsonify(status="not-favorite")


@app.route("/check-for-visited", methods=["GET"])
def check_for_visited():
    """Check for a visited restaurant for a user"""

    yelp_location_id = request.args.get("yelp-id")
    user_id = session["user_id"]

    visited = db.session.query(Visited_Restaurant).filter(Visited_Restaurant.yelp_location_id==yelp_location_id,
                                                            Visited_Restaurant.user_id==user_id).all()

    if visited:
        return jsonify(status="visited", id=yelp_location_id)

    else:
        return jsonify(status="not-visited")


@app.route('/profile')
def show_profile():
    """User profile page"""

    user_id = session.get("user_id")

    if user_id:
        user = db.session.query(User).filter(User.user_id==user_id).one()
        return render_template("profile.html", user=user)

    else:
        flash("Sorry, you must be logged in to access your profile.")
        return redirect("/login")


@app.route("/favorites")
def display_favorites():
    """Displays page of favorite restaurants."""

    user_id = session.get("user_id")

    if user_id:
        favorites = db.session.query(Favorite_Restaurant.yelp_location_id).filter(Favorite_Restaurant.user_id==user_id).all()
        restaurants = get_restaurants_from_db(favorites)
        return render_template("favorites.html", restaurants=restaurants)

    else:
        flash("Sorry, you must be logged in to access your favorites.")
        return redirect("/login")


@app.route("/visited")
def display_visited():
    """Displays page of visited restaurants."""

    user_id = session.get("user_id")

    if user_id:
        visited_restaurants = db.session.query(Visited_Restaurant.yelp_location_id).filter(Visited_Restaurant.user_id==user_id).all()
        restaurants = get_restaurants_from_db(visited_restaurants)
        return render_template("visited.html", restaurants=restaurants)

    else:
        flash("Sorry, you must be logged in to access your visited restaurants.")
        return redirect("/login")


@app.route("/about")
def display_about():
    return render_template("about.html")


@app.route("/check-for-logged-in", methods=["GET"])
def check_for_logged_in():
    """Checks if user is logged in."""

    if session.get("user_id"):
        return jsonify(status="logged-in")

    else:
        return jsonify(status="logged-out")


def get_restaurants_from_db(list_of_yelp_ids):
    """Grab restaurants from DB, returns a list of restaurant dictionaries."""

    restaurants = []

    for id in list_of_yelp_ids:
        restaurant = db.session.query(Restaurant).filter(Restaurant.yelp_location_id==id).one()
        restaurants.append(restaurant)

    return restaurants

if __name__ == "__main__":
# using the Flask Debug bar, including setting debug = True
    app.debug = True
    DebugToolbarExtension(app)

    connect_to_db(app)
    db.create_all()

    app.run()
