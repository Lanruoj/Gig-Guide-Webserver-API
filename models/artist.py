from main import db


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String())

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