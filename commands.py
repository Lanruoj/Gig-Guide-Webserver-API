from re import A
import os
from flask import Blueprint, current_app
from main import db, bcrypt
from models.artist import Artist
from models.gig import Gig
from models.user import User
from models.venue import Venue
from datetime import datetime
from models.watch_venue import WatchVenue
from models.watch_artist import WatchArtist
from models.country import Country
from models.state import State
from models.city import City
from models.genre import Genre
from models.artist_genre import ArtistGenre
from models.venue_type import VenueType


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
        country_id = 1
    )
    db.session.add(test_artist1)
    test_artist2 = Artist(
        name = "Sweet Whirl",
        country_id = 1
    )
    db.session.add(test_artist2)
    test_artist3 = Artist(
        name = "Jordan Ireland",
        country_id = 1
    )
    db.session.add(test_artist3)
    test_artist4 = Artist(
        name = "King Krule"
    )
    db.session.add(test_artist4)
    test_artist5 = Artist(
        name = "Arthur Russell"
    )
    db.session.add(test_artist5)
    test_artist6 = Artist(
        name = "Connan Mockasin"
    )
    db.session.add(test_artist6)
    test_artist7 = Artist(
        name = "Blake Mills"
    )
    db.session.add(test_artist7)
    test_artist8 = Artist(
        name = "Julian Lage"
    )
    db.session.add(test_artist8)
    test_artist9 = Artist(
        name = "Mulatu Astatke"
    )
    db.session.add(test_artist9)
    db.session.commit()

    # VENUE TYPE SEEDS
    vt1 = VenueType(
        name = "Music venue"
    )
    db.session.add(vt1)
    vt2 = VenueType(
        name = "Pub"
    )
    db.session.add(vt2)
    vt3 = VenueType(
        name = "Concert hall"
    )
    db.session.add(vt3)
    db.session.add(vt2)
    vt4 = VenueType(
        name = "Stadium"
    )
    db.session.add(vt4)
    vt5 = VenueType(
        name = "Divebar"
    )
    db.session.add(vt5)
    vt6 = VenueType(
        name = "Restaurant"
    )
    db.session.add(vt6)
    vt7 = VenueType(
        name = "Theatre"
    )
    db.session.add(vt7)
    vt8 = VenueType(
        name = "Hotel"
    )
    db.session.add(vt8)
    vt9 = VenueType(
        name = "Amphitheatre"
    )
    db.session.add(vt9)
    vt10 = VenueType(
        name = "House"
    )
    db.session.add(vt10)
    vt11 = VenueType(
        name = "Warehouse"
    )
    db.session.add(vt11)
    vt12 = VenueType(
        name = "Jazz club"
    )
    db.session.add(vt12)
    vt13 = VenueType(
        name = "Nightclub"
    )
    db.session.add(vt13)
    vt14 = VenueType(
        name = "Discotheque"
    )
    db.session.add(vt14)
    vt15 = VenueType(
        name = "Festival"
    )
    db.session.add(vt15)
    vt15 = VenueType(
        name = "Bowls Club"
    )
    db.session.add(vt15)
    vt15 = VenueType(
        name = "Park"
    )
    db.session.add(vt15)
    vt16 = VenueType(
        name = "Beach"
    )
    db.session.add(vt16)
    vt17 = VenueType(
        name = "Record/music store"
    )
    db.session.add(vt17)
    db.session.commit()

    # VENUE SEEDS
    test_venue1 = Venue(
        name = "The Gasometer Hotel",
        street_address = "484 Smith St",
        city_id = 1,
        venue_type_id = 1
    )
    db.session.add(test_venue1)
    test_venue2 = Venue(
        name = "The Forum",
        street_address = "154 Flinders St",
        city_id = 1,
        venue_type_id = 7
    )
    db.session.add(test_venue2)
    test_venue3 = Venue(
        name = "The Jazzlab",
        street_address = "27 Leslie street",
        city_id = 1,
        venue_type_id = 12
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
    db.session.add(wv3)
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

    # GENRE SEEDS
    genre1 = Genre(
        name = "Pop"
    )
    db.session.add(genre1)
    genre2 = Genre(
        name = "Rock"
    )
    db.session.add(genre2)
    genre3 = Genre(
        name = "Jazz"
    )
    db.session.add(genre3)
    genre4 = Genre(
        name = "Metal"
    )
    db.session.add(genre4)
    genre5 = Genre(
        name = "Psychedelic"
    )
    db.session.add(genre5)
    genre6 = Genre(
        name = "Punk"
    )
    db.session.add(genre6)
    genre7 = Genre(
        name = "Folk"
    )
    db.session.add(genre7)
    genre8 = Genre(
        name = "World"
    )
    db.session.add(genre8)
    genre9 = Genre(
        name = "Blues"
    )
    db.session.add(genre9)
    genre10 = Genre(
        name = "Funk"
    )
    db.session.add(genre10)
    genre11 = Genre(
        name = "Hip-hop"
    )
    db.session.add(genre11)
    genre12 = Genre(
        name = "Soul"
    )
    db.session.add(genre12)
    genre13 = Genre(
        name = "RnB"
    )
    db.session.add(genre13)
    genre14 = Genre(
        name = "House"
    )
    db.session.add(genre14)
    genre15 = Genre(
        name = "Electronica"
    )
    db.session.add(genre15)
    genre16 = Genre(
        name = "Disco"
    )
    db.session.add(genre16)
    genre17 = Genre(
        name = "Techno"
    )
    db.session.add(genre17)
    genre18 = Genre(
        name = "Classical"
    )
    db.session.add(genre18)
    genre19 = Genre(
        name = "Ambient"
    )
    db.session.add(genre19)
    genre20 = Genre(
        name = "Country"
    )
    db.session.add(genre20)
    genre21 = Genre(
        name = "Reggae"
    )
    db.session.add(genre21)
    db.session.commit()

    # ARTIST_GENRE SEEDS
    ag1 = ArtistGenre(
        artist_id = 1,
        genre_id = 1
    )
    db.session.add(ag1)
    ag1 = ArtistGenre(
        artist_id = 1,
        genre_id = 2
    )
    db.session.add(ag1)
    db.session.commit()

    print("Tables seeded")