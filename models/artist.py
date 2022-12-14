from main import db


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(db.String())

    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))

    artist_genres = db.relationship(
        "ArtistGenre",
        back_populates="ag_artist",
        cascade="all, delete"
    )

    country = db.relationship(
        "Country",
        back_populates="artist_country"
    )

    artist_wa = db.relationship(
        "WatchArtist",
        back_populates="artist",
        cascade="all, delete"
    )

    performances = db.relationship(
        "Performance",
        backref="a_gig",
        cascade="all, delete"
    )