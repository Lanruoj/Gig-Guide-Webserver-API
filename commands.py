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
        name = "The Jazz Lab",
        street_address = "27 Leslie street",
        city = "Brunswick",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue2)
    db.session.commit()

    test_gig = Gig(
        title = "Gregor",
        description = "Gregor plays Destiny at the Gaso!",
        start_time = datetime(year=2022, month=9, day=17, hour=18),
        price = 20,
        timestamp = datetime.now(),
        artists = "Gregor",
        venue_id = 1,
        user_id = 1
    )
    db.session.add(test_gig)
    db.session.commit()

    print("Tables seeded")