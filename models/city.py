from main import db


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"), nullable=False)

    state = db.relationship(
        "State",
        back_populates="city"
    )

    venue_city = db.relationship(
        "Venue",
        back_populates="city"
    )

