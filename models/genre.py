from main import db


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    genre_ag = db.relationship(
        "ArtistGenre",
        back_populates="ag_genre"
    )