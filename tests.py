"""Test suite for BobaFetch app."""

import os
import unittest
from server import app, get_restaurants_from_db
from model import connect_to_db, db, User, Restaurant, Favorite_Restaurant, Visited_Restaurant
import yelp_call

CONSUMER_KEY = os.environ['YELP_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['YELP_CONSUMER_SECRET']
TOKEN = os.environ['YELP_TOKEN']
TOKEN_SECRET = os.environ['YELP_TOKEN_SECRET']

class BobaFetchUnitTestCase(unittest.TestCase):
    """Tests for BobaFetch app for functions that don't require sessions."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Create secret key to access session
        app.secret_key = "TESTINGBOBAFETCH"

        # Connect to fake database
        connect_to_db(app, 'postgresql:///bobafetchfaker')

        app.config['TESTING'] = True
    
    #############################################################################
    # API tests
    def test_request_restaurants(self):
        """Does the request return a list of yelp_location_ids?"""

        pass

    #############################################################################
    # route tests (only template rendering)

    def test_landing_page(self):
        """Does the landing page load correctly?"""

        result = self.client.get('/')
        self.assertIn('div class="jumbotron"', result.data)

    def test_alt_landing_page(self):
        """Does the alternate landing page load correctly?"""

        result = self.client.get('/alanding')
        self.assertIn('div class="jumbotron"', result.data)
        self.assertNotIn('div class="navbar-header"', result.data)

    def test_sign_up_form(self):
        """Does the sign-up form load?"""

        result = self.client.get('/signup')
        self.assertIn("Create my account!", result.data)

    def test_login_form(self):
        """Does the login form load?"""

        result = self.client.get('/login')
        self.assertIn("<h1>Login</h1>", result.data)

    #############################################################################
    # data query/update tests
    def test_get_restaurants_from_db(self):
        """Does query return a list of restaurant objects?"""

        pass

    def test_save_restaurants(self):
        """Do the restaurants get saved?"""

        pass

    #############################################################################
    # instance tests

    #############################################################################
    # remaining helper function tests
    def test_get_radius(self):
        """Does the radius get used correctly?"""

        assert yelp_call.get_radius(60, 6)==3621.015


class BobaFetchIntegrationTestCase(unittest.TestCase):
    """Tests for BobaFetch app for functions that require sessions."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Create secret key to access session
        app.secret_key = "TESTINGBOBAFETCH"

        # Connect to fake database
        connect_to_db(app, 'postgresql:///bobafetchfaker')

        app.config['TESTING'] = True

        # initiate a session
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = '1'

    #############################################################################
    # route tests
    def test_show_profile(self):
        """Does the profile page load?"""

        result = self.client.get('/profile')
        self.assertIn("anli", result.data)
        self.assertIn("Profile", result.data)

    #############################################################################
    # data query/update tests
    def test_sign_up_process(self):
        """Does the sign-up process create a new user in the db
        and set the session key correctly with user_id?"""

        pass

    def test_login_process(self):
        """Does the login process correctly check for users/passwords,
        add a session key if correct, and redirect to the landing page?"""

        pass

    def test_logout(self):
        """Does the logout process remove the session key and redirect to the landing page?"""

        pass

    def test_show_results(self):
        """Does show_results grab the correct information from the form,
        get restaurants from the DB, and render the correct page when results are available?"""

        pass

    def test_show_map(self):
        """Does the map route get the correct request, get result
        from the database, and render the map html correctly?"""

        pass

    def test_add_to_favorites(self):
        """Does this function successfully add a new favorite restaurant?"""

        pass

    def test_check_for_favorite(self):
        """Does this function successfully check for an existing favorite
        restaurant?"""

        pass

    def test_add_to_visited(self):
        """Does this function successfully add a new visited restaurant?"""

        pass

    def test_check_for_visited(self):
        """Does this function successfully check for an existing visited
        restaurant?"""

        pass

    def test_display_favorites(self):
        """Does the list of favorite restaurants display?"""

        pass

    def test_display_visited(self):
        """Does the list of visited restaurants display?"""

        pass

    #############################################################################
    # instance tests

    #############################################################################
    # remaining helper function tests



if __name__ == "__main__":
    unittest.main()