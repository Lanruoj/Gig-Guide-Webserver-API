from main import ma
from marshmallow import fields
from schemas.country_schema import CountrySchema


class StateSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "country_id", "country")

    country_id = ma.Integer(required=True)

    country = fields.Nested(CountrySchema)

state_schema = StateSchema()
states_schema = StateSchema(many=True)