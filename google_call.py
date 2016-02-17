import googlemaps
import os

SERVER_KEY = os.environ['GOOGLE_SERVER_KEY']
# instantiate a Client with the API key

# should eventually take in at least location information for both origin and destination
def request_directions():
    """Sends request for directions, returns..."""

    client = googlemaps.Client(SERVER_KEY)

    # generate a distance_matrix with start and end locations
    # time-box exploring this in the console, if it doesn't work
    # you can try just doing directions one way and then the other
    # either way, it seems like you'll have to add up the results

    # CONSOLE TESTS
    # it's being wierd and generating seemingly extraneous entries in the list of elements; try with 3 each of origin and destination to see if the pattern is at least predictable
    # might be because my start and ends are the same? JS example response seems to give 4 sets of duration/distance each (both ways)
     

    # FIXME: these locations are hardcoded now
    # origin should be the same one sent to Yelp
    # destination should be the location received from Yelp
    origin = '1617 Hess Road, Redwood City, CA 94061'
    destination = '211 S Whisman Rd, Mountain View, CA 94041'

    # directions both ways:
    # ? look into waypoints param in .directions; maybe you could have origin and
    # destination be home/start and waypoint be restaurant
    directions_there = client.directions(origin, destination, mode='walking', units='imperial')
    directions_back = client.directions(destination, origin, mode='walking', units='imperial')

    # pull the useful stuff out of the map?

    # possibly should do this in a separate file/function
    # if possible, render both routes on the displayed map

def display_map():
    """Displays route(s) on the map(s)"""
