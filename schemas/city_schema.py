from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class CitySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "state_id")


city_schema = CitySchema()
cities_schema = CitySchema(many=True)