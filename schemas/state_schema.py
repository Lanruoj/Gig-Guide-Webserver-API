from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class StateSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "country_id")

state_schema = StateSchema()
states_schema = StateSchema(many=True)