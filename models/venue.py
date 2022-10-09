from main import db


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    street_address = db.Column(db.String(), nullable=False)

    venue_type_id = db.Column(db.Integer, db.ForeignKey("venue_types.id"))  
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)

    city = db.relationship(
        "City",
        back_populates="venue_city"
    )

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

    venue_type = db.relationship(
        "VenueType",
        back_populates="venues"
    )
    
