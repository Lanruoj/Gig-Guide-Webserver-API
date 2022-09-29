from main import ma
from marshmallow import fields
from marshmallow.validate import Length, ContainsOnly


class GigSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "description", "artists", "venue", "start_time", "price", "tickets_url", "timestamp", "is_deleted", "is_expired", "venue_id", "user_id", "user", "performances")
        load_only = ["user_id", "performances"]

    title = ma.String(validate=Length(max=32))
    description = ma.String(validate=Length(max=100))
    artists = ma.String(required=True)
    start_time = ma.DateTime(required=True)
    price = ma.Integer()
    tickets_url = ma.URL()
    venue_id = ma.Integer(required=True)

    performances = fields.List(fields.Nested("PerformanceSchema"))
    venue = fields.Pluck("VenueSchema", "name")
    user = fields.Pluck("UserSchema", "username")

gig_schema = GigSchema()
gigs_schema = GigSchema(many=True)