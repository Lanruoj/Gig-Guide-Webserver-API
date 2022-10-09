from main import db


class VenueType(db.Model):
    __tablename__ = "venue_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    venues = db.relationship(
        "Venue",
        back_populates="venue_type"
    )