from main import ma


class CountrySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name")

    name = ma.String(required=True)

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)