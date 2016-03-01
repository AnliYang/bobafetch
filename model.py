"""Models and database functions for Boba Fetch!"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of boba running website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    favorite_restaurants = db.relationship("Restaurant",
                                           secondary='favorite_restaurants',
                                           backref='favoritors')

    visited_restaurants = db.relationship("Restaurant",
                                          secondary='visited_restaurants',
                                          backref='visitors')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Restaurant(db.Model):
    """Restaurants saved by users.

    Used for favorite restaurants, routes done (visited restaurants), or both.

    Uses yelp_location_id as the primary_key"""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yelp_location_id = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    # address = db.Column(db.String(200), nullable=False)
    display_address = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip5 = db.Column(db.String(5), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    yelp_url = db.Column(db.String(2000), nullable=False)
    image_url = db.Column(db.String(2000), nullable=False)
    mobile_url = db.Column(db.String(2000), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    rating_img_url = db.Column(db.String(2000), nullable=False)
    review_count = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant yelp_location_id=%s>" % self.yelp_location_id


class Favorite_Restaurant(db.Model):
    """Restaurants favorited by users."""

    __tablename__ = "favorite_restaurants"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<favorite_id=%s: user %s favorited restaurant %s>" % (self.favorite_id,
                                                                      self.user_id,
                                                                      self.restaurant_id)


class Visited_Restaurant(db.Model):
    """Restaurants visited by users.

    A user can visit the same restaurant multiple times."""

    __tablename__ = "visited_restaurants"

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    distance_miles = db.Column(db.Float, nullable=False)
    running_time_minutes = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<visitor_id=%s: user %s visited restaurant %s>" % (self.visit_id,
                                                                   self.user_id,
                                                                   self.restaurant_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bobafetch'
    db.app = app
    db.init_app(app)


# FIXME
def seed(app):
    """Sample data for testing. To be removed after stuff is all hooked up."""

    anli = User(email='anli@anli.com',
                password='anli',
                first_name='anli',
                last_name='yang')
    print "anli created"

    rest = Restaurant(yelp_location_id='comebuy-drinks-redwood-city',
                      name='Comebuy Drinks',
                      display_address='2074 Broadway',
                      city='Redwood City',
                      state='CA',
                      zip5='94063',
                      latitude=37.4868,
                      longitude=-122.22766,
                      yelp_url='http://www.yelp.com/biz/comebuy-drinks-redwood-city?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=TLw32XZLal2SNHLl-eyLKg',
                      image_url='http://s3-media4.fl.yelpcdn.com/bphoto/qm8MD51QFahwiwNtMIyC2A/ms.jpg',
                      mobile_url='http://m.yelp.com/biz/comebuy-drinks-redwood-city?utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=TLw32XZLal2SNHLl-eyLKg',
                      rating=4.0,
                      rating_img_url='http://s3-media4.fl.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png',
                      review_count=39)
    print "rest created"

    fav = Favorite_Restaurant(user_id=1,
                              restaurant_id=1)
    print "fav created"

    vis = Visited_Restaurant(user_id=1,
                             restaurant_id=1,
                             distance_miles=3.20,
                             running_time_minutes=30)
    print "vis created"

    db.session.add(anli)
    db.session.add(rest)
    print "anli and rest added to db"
    # user and restaurant need to be committed before creating favs or visiteds
    db.session.commit()
    print "anli and rest committed"

    db.session.add(fav)
    db.session.add(vis)
    print "fav and vis added to db"
    db.session.commit()
    print "fav and vis committed!"

    # to reseed:
    # in terminal:
        # dropdb bobafetch,
        # createdb bobafetch,
        # python server.py
        # python model.py


if __name__ == "__main__":
    # if module run in interactive mode, we can work with database directly

    from server import app
    connect_to_db(app)
    seed(app)
    print "Connected to DB."
