from main import ma
from marshmallow import fields
from marshmallow.validate import Length
from schemas.country_schema import CountrySchema


class StateSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "country_id", "country")

    country = fields.Nested(CountrySchema)

state_schema = StateSchema()
states_schema = StateSchema(many=True)