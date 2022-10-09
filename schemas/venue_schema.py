from main import ma
from marshmallow import fields
from marshmallow.validate import ContainsOnly
from string import ascii_lowercase, ascii_uppercase, digits
from schemas.city_schema import CitySchema
from schemas.venue_type_schema import VenueTypeSchema


alphanumeric = ascii_uppercase + ascii_lowercase + digits


class VenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "venue_type_id", "venue_type", "street_address", "city_id", "city", "venue_gigs")
    
    name = ma.String(required=True)
    street_address = ma.String(required=True, validate=ContainsOnly(alphanumeric + " /-,()&."))

    venue_type = fields.Nested(VenueTypeSchema)

    city = fields.Nested(CitySchema)

    venue_gigs = fields.List(fields.Nested("GigSchema"))

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)