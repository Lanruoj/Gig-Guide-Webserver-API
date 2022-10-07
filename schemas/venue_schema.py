from main import ma
from marshmallow import fields
from marshmallow.validate import Length, ContainsOnly
from string import ascii_lowercase, ascii_uppercase, digits
from schemas.city_schema import CitySchema


alphanumeric = ascii_uppercase + ascii_lowercase + digits


class VenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "street_address", "city_id", "city", "type", "venue_gigs")
        load_only = ["city_id"]
    
    name = ma.String(required=True)
    street_address = ma.String(required=True, validate=ContainsOnly(alphanumeric + " /-,()&."))
    type = ma.String()

    city = fields.Nested(CitySchema)

    venue_gigs = fields.List(fields.Nested("GigSchema"))

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)