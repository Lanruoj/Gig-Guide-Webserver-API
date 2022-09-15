from main import ma
from marshmallow import fields


class GigSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "description", "start_time", "price", "timestamp", "venue_id", "venue", "user_id", "user", "artist_id", "artist")
    venue = fields.Nested("VenueSchema")
    # artists = fields.List(fields.Nested("ArtistSchema"))
    artist = fields.Nested("ArtistSchema")
    user = fields.Nested("UserSchema")
    

gig_schema = GigSchema()
gigs_schema = GigSchema(many=True)