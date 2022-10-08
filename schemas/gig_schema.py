from main import ma
from marshmallow import fields
from marshmallow.validate import Length, ContainsOnly


class GigSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "title", "gig_venue", "artists", "description", "start_time", "price", "tickets_url", "date_added", "posted_by", "is_expired", "venue_id", "user_id", "performances", "gig_artists")

    title = ma.String(required=True, validate=Length(max=50))
    description = ma.String(validate=Length(max=100))
    artists = ma.String(required=True)
    start_time = ma.DateTime(required=True)
    price = ma.Integer()
    tickets_url = ma.URL()
    venue_id = ma.Integer(required=True)

    performances = fields.List(fields.Nested("PerformanceSchema"))
    gig_venue = fields.Pluck("VenueSchema", "name")
    posted_by = fields.Pluck("UserSchema", "username")

gig_schema = GigSchema()
gigs_schema = GigSchema(many=True)