"""Models and database functions for BobaFetch!"""

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

    Uses yelp_location_id as the primary_key."""

    __tablename__ = "restaurants"

    yelp_location_id = db.Column(db.String(500), nullable=False, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    street1 = db.Column(db.String(200), nullable=False)
    street2 = db.Column(db.String(200), nullable=True)
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

    def create_restaurant_geojson(self):
        """Create GeoJSON-ready from restaurant object."""

        restaurant_geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude]
            },
            "properties": {
                "yelp-location-id": self.yelp_location_id,
                "name": self.name,
                "url": self.yelp_url,
                "street1": self.street1,
                "city": self.city,
                "state": self.state,
                "zip": self.zip5,
                "image": self.image_url,
                "marker-symbol": "rocket"
                }
        }

        return restaurant_geojson


class Favorite_Restaurant(db.Model):
    """Restaurants favorited by users."""

    __tablename__ = "favorite_restaurants"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    yelp_location_id = db.Column(db.String(500), db.ForeignKey('restaurants.yelp_location_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<favorite_id=%s: user %s favorited restaurant %s>" % (self.favorite_id,
                                                                      self.user_id,
                                                                      self.yelp_location_id)


class Visited_Restaurant(db.Model):
    """Restaurants visited by users.

    A user can visit the same restaurant multiple times."""

    __tablename__ = "visited_restaurants"

    visit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    yelp_location_id = db.Column(db.String(500), db.ForeignKey('restaurants.yelp_location_id'), nullable=False)
    distance_miles = db.Column(db.Float, nullable=True)
    running_time_minutes = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<visitor_id=%s: user %s visited restaurant %s>" % (self.visit_id,
                                                                   self.user_id,
                                                                   self.yelp_location_id)


##############################################################################
# Helper functions
def connect_to_db(app, db_uri=None):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///bobafetch'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    print "Connected to DB."


if __name__ == "__main__":
    # run module in interactive mode to work with database directly
    from server import app
    connect_to_db(app)
    # seed(app)
    print "Connected to DB."
