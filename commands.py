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
        name = "The Jazzlab",
        street_address = "27 Leslie street",
        city = "Brunswick",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue2)
    db.session.commit()

    test_gig = Gig(
        title = "Gregor [EXPIRED]",
        description = "Gregor plays Destiny at the Forum!",
        start_time = datetime(year=2022, month=9, day=17, hour=18),
        price = 20,
        date_added = datetime.now(),
        artists = "Gregor",
        venue_id = 2,
        user_id = 1
    )
    db.session.add(test_gig)
    test_gig1 = Gig(
        title = "Jordan Ireland at the Jazzlab [ACTIVE]",
        description = "Jordan Ireland plays at the Jazzlab!",
        start_time = datetime(year=2023, month=9, day=17, hour=18),
        price = 20,
        tickets_url = "https://tickets.gig.com",
        date_added = datetime.now(),
        artists = "Jordan Ireland",
        venue_id = 3,
        user_id = 1
    )
    db.session.add(test_gig1)
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