from marshmallow import EXCLUDE

from ma import ma

from models.rent_models import RentModel


class RentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RentModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE
