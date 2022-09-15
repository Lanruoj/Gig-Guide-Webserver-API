from main import db


class Artist(db.Model):
    __tablename__ = "artists"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    genre = db.Column(db.String())
