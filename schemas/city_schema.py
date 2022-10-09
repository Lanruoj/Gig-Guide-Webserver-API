from main import ma
from marshmallow import fields
from schemas.state_schema import StateSchema


class CitySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "state_id", "state")

    state = fields.Nested(StateSchema)


city_schema = CitySchema()
cities_schema = CitySchema(many=True)