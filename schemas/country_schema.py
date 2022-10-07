from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class CountrySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name")

    # states... ?

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)