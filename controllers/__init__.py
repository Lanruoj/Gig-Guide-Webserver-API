from controllers.auth_controller import auth
from controllers.gig_controller import gigs
from controllers.artist_controller import artists
from controllers.venue_controller import venues
from controllers.user_controller import users

registerable_controllers = [auth, users, gigs, artists, venues]