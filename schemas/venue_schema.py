from main import ma
from marshmallow import fields


class VenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "street_address", "city", "state", "country", "type", "gigs")
    
    gigs = fields.List(fields.Nested("GigSchema"))

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)