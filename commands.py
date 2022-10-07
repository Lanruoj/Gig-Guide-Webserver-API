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
from models.watch_artist import WatchArtist
from models.country import Country
from models.state import State
from models.city import City



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
    # COUNTRY SEEDS
    country1 = Country(
        name = "Australia"
    )
    db.session.add(country1)
    db.session.commit()
    # STATE SEEDS
    state1 = State(
        name = "Victoria",
        country_id = 1
    )
    db.session.add(state1)
    db.session.commit()
    # CITY SEEDS
    city1 = City(
        name = "Melbourne",
        state_id = 1
    )
    db.session.add(city1)
    db.session.commit()

    # USER SEEDS
    admin = User(
        username = "admin",
        password = bcrypt.generate_password_hash(current_app.config["ADMIN_PASSWORD"]).decode("utf-8"),
        email = "admin@email.com",
        first_name = "Admin",
        last_name = "User",
        admin = True
    )
    db.session.add(admin)
    user1 = User(
        username = "user",
        password = bcrypt.generate_password_hash(current_app.config["USER_PASSWORD"]).decode("utf-8"),
        email = "user@email.com",
        first_name = "User",
        last_name = "Test",
        admin = False
    )
    db.session.add(user1)
    user2 = User(
        username = "punter",
        password = bcrypt.generate_password_hash(current_app.config["PUNTER_PASSWORD"]).decode("utf-8"),
        email = "punter@email.com",
        first_name = "Punter",
        last_name = "Smith",
        admin = False
    )
    db.session.add(user2)
    db.session.commit()

    # ARTIST SEEDS
    test_artist1 = Artist(
        name = "Gregor",
        genre = "Alternative Pop"
    )
    db.session.add(test_artist1)
    test_artist2 = Artist(
        name = "Sweet Whirl",
        genre = "Alternative Pop"
    )
    db.session.add(test_artist2)
    test_artist3 = Artist(
        name = "Jordan Ireland",
        genre = "Folk"
    )
    db.session.add(test_artist3)
    test_artist4 = Artist(
        name = "King Krule",
        genre = "Punk"
    )
    db.session.add(test_artist4)
    test_artist5 = Artist(
        name = "Arthur Russell",
        genre = "Experimental"
    )
    db.session.add(test_artist5)
    test_artist6 = Artist(
        name = "Connan Mockasin",
        genre = "Alternative Rock"
    )
    db.session.add(test_artist6)
    test_artist7 = Artist(
        name = "Blake Mills",
        genre = "Alternative Rock"
    )
    db.session.add(test_artist7)
    test_artist8 = Artist(
        name = "Julian Lage",
        genre = "Jazz"
    )
    db.session.add(test_artist8)
    test_artist9 = Artist(
        name = "Mulatu Astatke",
        genre = "World"
    )
    db.session.add(test_artist9)
    db.session.commit()

    # VENUE SEEDS
    test_venue1 = Venue(
        name = "The Gasometer Hotel",
        street_address = "484 Smith St",
        city = "Collingwood",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue1)
    test_venue2 = Venue(
        name = "The Forum",
        street_address = "154 Flinders St",
        city = "Melbourne",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue2)
    test_venue3 = Venue(
        name = "The Jazzlab",
        street_address = "27 Leslie street",
        city = "Brunswick",
        state = "Victoria",
        country = "Australia"
    )
    db.session.add(test_venue3)
    db.session.commit()

    # GIG SEEDS
    test_gig1 = Gig(
        title = "Gregor [EXPIRED]",
        description = "Gregor plays Destiny at the Forum!",
        start_time = datetime(year=2022, month=9, day=17, hour=18),
        price = 50,
        date_added = datetime.now(),
        artists = "Gregor",
        venue_id = 2,
        user_id = 2
    )
    db.session.add(test_gig1)
    test_gig2 = Gig(
        title = "Jordan Ireland at the Jazzlab [ACTIVE]",
        description = "Jordan Ireland plays at the Jazzlab!",
        start_time = datetime(year=2023, month=9, day=17, hour=18),
        price = 20,
        tickets_url = "https://tickets.gig.com",
        date_added = datetime.now(),
        artists = "Jordan Ireland",
        venue_id = 3,
        user_id = 3
    )
    db.session.add(test_gig2)
    test_gig3 = Gig(
        title = "Sweet Whirl at the Forum [ACTIVE]",
        description = "...",
        start_time = datetime(year=2023, month=5, day=17, hour=18),
        price = 55,
        tickets_url = "https://tickets.gig.com",
        date_added = datetime.now(),
        artists = "Sweet Whirl",
        venue_id = 2,
        user_id = 3
    )
    db.session.add(test_gig3)
    test_gig4 = Gig(
        title = "Gregor at the Gasometer [ACTIVE]",
        description = "...",
        start_time = datetime(year=2022, month=12, day=13, hour=18),
        price = 15,
        tickets_url = "https://tickets.gig.com",
        date_added = datetime.now(),
        artists = "Gregor",
        venue_id = 1,
        user_id = 2
    )
    db.session.add(test_gig4)
    db.session.commit()

    # WATCHVENUE SEEDS
    wv1 = WatchVenue(
        user_id = 2,
        venue_id = 1
    )
    db.session.add(wv1)
    wv2 = WatchVenue(
        user_id = 2,
        venue_id = 3
    )
    db.session.add(wv2)
    wv3 = WatchVenue(
        user_id = 3,
        venue_id = 1
    )
    db.session.add(wv2)
    wv4 = WatchVenue(
        user_id = 3,
        venue_id = 2
    )
    db.session.add(wv4)
    db.session.commit()

    # WATCHARTIST SEEDS
    wa1 = WatchArtist(
        user_id = 2,
        artist_id = 2
    )
    db.session.add(wa1)
    wa2 = WatchArtist(
        user_id = 3,
        artist_id = 3
    )
    db.session.add(wa2)
    wa3 = WatchArtist(
        user_id = 3,
        artist_id = 1
    )
    db.session.add(wa3)
    db.session.commit()

    print("Tables seeded")