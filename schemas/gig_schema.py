from main import ma
from marshmallow import fields


class GigSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "artists", "venue", "description", "start_time", "price", "timestamp", "venue_id", "user_id", "user", "performances")
        load_only = ["venue_id", "user_id", "performances"]
    performances = fields.List(fields.Nested("PerformanceSchema"))
    # venue = fields.Nested("VenueSchema", only=("name",))
    # user = fields.Nested("UserSchema", only=("username",))
    venue = fields.Pluck("VenueSchema", "name")
    user = fields.Pluck("UserSchema", "username")

gig_schema = GigSchema()
gigs_schema = GigSchema(many=True)