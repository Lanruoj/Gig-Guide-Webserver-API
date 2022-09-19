from re import A
import os
from flask import Blueprint, current_app
from main import db, bcrypt
from models.artist import Artist
from models.gig import Gig
from models.user import User
from models.venue import Venue
from models.performance import Performance
from datetime import datetime
from models.watch_venue import WatchVenue
from schemas.watch_venue_schema import watch_venue_schema, watch_venues_schema



db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_db():
    admin = User(
        username = "admin",
        password = bcrypt.generate_password_hash(current_app.config["ADMIN_PASSWORD"]).decode("utf-8"),
        email = "admin@email.com",
        first_name = "Admin",
        last_name = "User",
        admin = True
    )
    db.session.add(admin)

    test_artist = Artist(
        name = "Gregor",
        genre = "Alt. pop"
    )
    db.session.add(test_artist)
    test_artist1 = Artist(
        name = "Sweet Whirl",
        genre = "Alt. pop"
    )
    db.session.add(test_artist1)
    test_artist2 = Artist(
        name = "Jordan Ireland",
        genre = "Folk"
    )
    db.session.add(test_artist2)
    db.session.commit()

    venue_template = Venue(
        name = "Name of venue",
        street_address = "Street address (123 Fake st)",
        city = "City/town",
        state = "State",
        country = "Country"
    )
    db.session.add(venue_template)
    test_venue = Venue(
        name = "The Gasometer Hotel",
        street_address = "484 Smith St",
        city = "Collingwood",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue)
    test_venue1 = Venue(
        name = "The Forum",
        street_address = "154 Flinders St",
        city = "Melbourne",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue1)
    test_venue2 = Venue(
        name = "The Jazz Lab",
        street_address = "27 Leslie street",
        city = "Brunswick",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue2)
    db.session.commit()

    gig_template = Gig(
        title = "Title of show (e.g Artist at the Venue)",
        description = "Description of the show, who the artists are and what punters can expect [optional]",
        start_time = datetime(year=2000, month=1, day=1, hour=0),
        price = 0,
        timestamp = datetime.now(),
        artists = "Name of artists seperated by a comma and space (e.g Artist1, Artist2, Artist3)",
        venue_id = 1,
        user_id = 1
    )
    db.session.add(gig_template)
    test_gig = Gig(
        title = "Gregor",
        description = "Gregor plays Destiny at the Gaso!",
        start_time = datetime(year=2022, month=9, day=17, hour=18),
        price = 20,
        timestamp = datetime.now(),
        artists = "Gregor",
        venue_id = 2,
        user_id = 1
    )
    db.session.add(test_gig)
    db.session.commit()

    wv = WatchVenue(
        user_id = 1,
        venue_id = 1
    )
    db.session.add(wv)
    wv2 = WatchVenue(
        user_id = 1,
        venue_id = 2
    )
    db.session.add(wv2)
    db.session.commit()

    print("Tables seeded")