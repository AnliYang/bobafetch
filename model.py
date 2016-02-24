"""Models and database functions for Boba Fetch!"""

from flask_sqlalchemy import SQLAlchemy

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
    # date_created =

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Restaurant(db.Model):
    """Restaurants saved by users.

    Used for favorite restaurants, routes done, or both.

    Uses yelp_location_id as the primary_key"""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yelp_location_id = db.Column(db.String(500), nullable=False)
    # date_created =

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant yelp_location_id=%s>" % self.yelp_location_id


class Favorite_Restaurant(db.Model):
    """Restaurants favorited by users."""

    __tablename__ = "favorite_restaurants"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))

    # date_created =


    user = 

    restaurant = 


# class Rating(db.Model):
#     """Rating of a movie by a user."""

#     __tablename__ = "ratings"

#     rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     score = db.Column(db.Integer)

#     # Define relationship to user
#     user = db.relationship("User",
#                            backref=db.backref("ratings", order_by=rating_id))

#     # Define relationship to movie
#     movie = db.relationship("Movie",
#                             backref=db.backref("ratings", order_by=rating_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
#             self.rating_id, self.movie_id, self.user_id, self.score)


# class Movie(db.Model):
#     """Movie on ratings website."""

#     __tablename__ = "movies"

#     movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     title = db.Column(db.String(100))
#     released_at = db.Column(db.DateTime)
#     imdb_url = db.Column(db.String(200))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Movie movie_id=%s title=%s>" % (self.movie_id, self.title)


# class Rating(db.Model):
#     """Rating of a movie by a user."""

#     __tablename__ = "ratings"

#     rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     movie_id = db.Column(db.Integer)
#     user_id = db.Column(db.Integer)
#     score = db.Column(db.Integer)

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
#             self.rating_id, self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bobafetch'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # if module run in interactive mode, we can work with database directly
    
    from server import app
    connect_to_db(app)
    print "Connected to DB."
