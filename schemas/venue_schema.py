from main import ma


class VenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "street_address", "city", "state", "country", "type")