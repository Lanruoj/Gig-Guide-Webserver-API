from main import db


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)

    city = db.relationship(
        "City",
        back_populates="state"
    )
    
    country = db.relationship(
        "Country",
        back_populates="state"
    )
