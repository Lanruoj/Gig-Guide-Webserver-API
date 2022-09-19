from main import db


class Performance(db.Model):
    __tablename__ = "performances"

    id = db.Column(db.Integer, primary_key=True)
    gig_id = db.Column(db.Integer, db.ForeignKey("gigs.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    
    gig = db.relationship(
        "Gig",
        backref="perf_gig",
        viewonly=True
    )
