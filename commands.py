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
    vic = State( # 1
        name = "Victoria",
        country_id = 1
    )
    db.session.add(vic)
    nsw = State( # 2
        name = "New South Wales",
        country_id = 1
    )
    db.session.add(nsw)
    qld = State( # 3
        name = "Queensland",
        country_id = 1
    )
    db.session.add(qld)
    nt = State( # 4
        name = "Northern Territory",
        country_id = 1
    )
    db.session.add(nt)
    sa = State( # 5
        name = "South Australia",
        country_id = 1
    )
    db.session.add(sa)
    wa = State( # 6
        name = "Western Australia",
        country_id = 1
    )
    db.session.add(wa)
    tas = State( # 7
        name = "Tasmania",
        country_id = 1
    )
    db.session.add(tas)
    act = State( # 8
        name = "Australian Capital Territory",
        country_id = 1
    )
    db.session.add(act)
    db.session.commit()

    # VICTORIA CITIES
    vic_cities = ["Melbourne", "Ararat", "Bairnsdale", "Benalla", "Ballarat", "Bendigo", "Dandenong", "Frankston", "Geelong", "Hamilton", "Horsham", "Latrobe City", "Melton", "Mildura", "Sale", "Shepparton", "Swan Hill", "Wangaratta", "Warrnambool", "Wodonga"]
    for name in vic_cities:
        city = City(
            name = name,
            state_id = 1
        )
        db.session.add(city)
    # NEW SOUTH WALES CITIES
    nsw_cities = ["Sydney", "Albury", "Armidale", "Bathurst", "Blue Mountains", "Broken Hill", "Campbelltown", "Cessnock", "Dubbo", "Goulburn", "Grafton", "Lithgow", "Liverpool", "Newcastle", "Orange", "Parramatta", "Penrith", "Queanbeyan", "Tamworth", "Wagga Wagga", "Wollongong", "City of Blacktown", "City of Canada Bay", "City of Coffs Harbour", "City of Fairfield", "City of Griffith", "City of Hawkesbury", "City of Lake Macquarie", "City of Lismore", "City of Maitland", "City of Randwick", "City of Ryde", "City of Shellharbour", "City of Shoalhaven", "City of Willoughby"]
    for name in nsw_cities:
        city = City(
            name = name,
            state_id = 2
        )
        db.session.add(city)
    # QUEENSLAND CITIES
    qld_cities = ["Brisbane", "Bundaberg", "Cairns", "Caloundra", "Gladstone", "Gold Coast", "Gympie", "Hervey Bay", "Ipswich", "Logan City", "Mackay", "Maryborough", "Mount Isa", "Rockhampton", "Sunshine Coast", "Toowoomba", "Townsville", "Charters Towers", "Redcliffe City", "Redland City", "Thuringowa", "Warwick"]
    for name in qld_cities:
        city = City(
            name = name,
            state_id = 3
        )
        db.session.add(city)
    # NORTHERN TERRITORY CITIES
    nt_cities = ["Darwin", "Palmerston"]
    for name in nt_cities:
        city = City(
            name = name,
            state_id = 4
        )
        db.session.add(city)
    # SOUTH AUSTRALIA CITIES
    sa_cities = ["Adelaide", "Mount Barker", "Mount Gambier", "Murray Bridge", "Port Adelaide", "Port Augusta", "Port Pirie", "Port Lincoln", "Victor Harbor", "Whyalla"]
    for name in sa_cities:
        city = City(
            name = name,
            state_id = 5
        )
        db.session.add(city)
    # WESTERN AUSTRALIA CITIES
    wa_cities = ["Perth", "Albany", "Bunbury", "Busselton", "Fremantle", "Geraldton", "Joondalup", "Kalgoorlie", "Karratha", "Mandurah", "City of Armadale", "City of Bayswater", "City of Canning", "City of Cockburn", "City of Gosnells", "City of Kalamunda", "City of Kwinana", "City of Melville", "City of Nedlands", "City of South Perth", "City of Stirling", "City of Subiaco", "City of Swan", "City of Wanneroo"]
    for name in wa_cities:
        city = City(
            name = name,
            state_id = 6
        )
        db.session.add(city)
    # TASMANIA CITIES
    tas_cities = ["Hobart", "Burnie", "Devonport", "Launceston"]
    for name in tas_cities:
        city = City(
            name = name,
            state_id = 7
        )
        db.session.add(city)
    # ACT CITIES
    canberra = City(
        name = "Canberra",
        state_id = 8
    )
    db.session.add(canberra)
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
        genre = "Alternative Pop",
        country_id = 1
    )
    db.session.add(test_artist1)
    test_artist2 = Artist(
        name = "Sweet Whirl",
        genre = "Alternative Pop",
        country_id = 1
    )
    db.session.add(test_artist2)
    test_artist3 = Artist(
        name = "Jordan Ireland",
        genre = "Folk",
        country_id = 1
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
        city_id = 1,
        type = "Music venue"
    )
    db.session.add(test_venue1)
    test_venue2 = Venue(
        name = "The Forum",
        street_address = "154 Flinders St",
        city_id = 1,
        type = "Music venue"
    )
    db.session.add(test_venue2)
    test_venue3 = Venue(
        name = "The Jazzlab",
        street_address = "27 Leslie street",
        city_id = 1,
        type = "Music venue"
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