from main import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    logged_in = db.Column(db.Boolean, default=False, nullable=False)

    watched_venues = db.relationship(
        "WatchVenue",
        backref="user_wv"
    )

    watched_artists = db.relationship(
        "WatchArtist",
        backref="user_wa"
    )
