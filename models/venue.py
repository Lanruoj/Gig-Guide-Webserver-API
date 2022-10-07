from main import db


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    street_address = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    type = db.Column(db.String())

    venue_gigs = db.relationship(
        "Gig",
        back_populates="gig_venue",
        cascade="all, delete"
    )

    venue_wv = db.relationship(
        "WatchVenue",
        back_populates="venue",
        cascade="all, delete"
    )
    
