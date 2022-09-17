from main import db


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String())

    performances = db.relationship(
        "Performance",
        backref="a_gig"
    )

    # gigs = db.relationship(
    #     "Gig",
    #     backref="artist_gigs"
    # )