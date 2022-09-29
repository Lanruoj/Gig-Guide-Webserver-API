from main import ma
from marshmallow import fields
from marshmallow.validate import Length, ContainsOnly
from string import ascii_lowercase, ascii_uppercase, digits


alphanumeric = ascii_uppercase + ascii_lowercase + digits


class VenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "street_address", "city", "state", "country", "type", "gigs")
    
    name = ma.String(required=True)
    street_address = ma.String(required=True, validate=ContainsOnly(alphanumeric + " /-,()&."))
    city = ma.String(required=True, validate=ContainsOnly(ascii_uppercase + ascii_lowercase + " '-."))
    state = ma.String(required=True, validate=ContainsOnly(ascii_uppercase + ascii_lowercase + " '-."))
    country = ma.String(required=True, validate=ContainsOnly(ascii_uppercase + ascii_lowercase + " '-."))
    type = ma.String()

    gigs = fields.List(fields.Nested("GigSchema"))

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)