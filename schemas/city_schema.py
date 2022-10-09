from main import ma
from marshmallow import fields
from schemas.state_schema import StateSchema


class CitySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "state_id", "state")

    name = ma.String(required=True)
    state_id = ma.Integer(required=True)
    
    state = fields.Nested(StateSchema)


city_schema = CitySchema()
cities_schema = CitySchema(many=True)