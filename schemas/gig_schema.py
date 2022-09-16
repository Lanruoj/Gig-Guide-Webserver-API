from main import ma
from marshmallow import fields


class GigSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "description", "start_time", "price", "timestamp", "venue_id", "venue", "user_id", "artists", "performances")
    performances = fields.List(fields.Nested("PerformanceSchema"))
    venue = fields.Nested("VenueSchema", only=("name",))
    

gig_schema = GigSchema()
gigs_schema = GigSchema(many=True)