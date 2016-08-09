"""Seed demo and/or test data into the DB."""

def seed_demo(app):
    """Seeding demo data."""

    demo_user = User(email='demo@bobafetch.com',
                     password = 'bobafetch',
                     first_name = 'Demo',
                     last_name = 'User')

    db.session.add(demo_user)
    db.session.commit()
    print "demo user created and committed to db"


def seed_test(app):
    """Sample data for testing. To be removed after stuff is all hooked up."""

    anli = User(email='anli@anli.com',
                password='anli',
                first_name='anli',
                last_name='yang')
    print "anli created"

    rest = Restaurant(yelp_location_id='comebuy-drinks-redwood-city',
                      name='Comebuy Drinks',
                      street1='2074 Broadway',
                      street2=None,
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
    print "restaurant created"

    db.session.add(anli)
    db.session.add(rest)
    print "anli and restaurant added to db"

    db.session.commit()
    print "anli and restaurant committed"

# to reseed:
# in terminal:
    # dropdb bobafetch,
    # createdb bobafetch,
    # python server.py
    # python model.py


if __name__ == "__main__":
    from server import app
    from model import db, connect_to_db, User, Restaurant

    connect_to_db(app, os.environ.get("DATABASE_URL"))
    seed_demo(app)
