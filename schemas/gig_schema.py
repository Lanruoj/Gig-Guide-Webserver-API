from main import ma
from marshmallow import fields


class GigSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "description", "start_time", "price", "timestamp", "venue_id", "venue", "user_id", "user", "performances")
    # venue = fields.Nested("VenueSchema")
    # artists = fields.List(fields.Nested("ArtistSchema"))
    # user = fields.Nested("UserSchema")
    performances = fields.List(fields.Nested("PerformanceSchema"))
    

gig_schema = GigSchema()
gigs_schema = GigSchema(many=True)