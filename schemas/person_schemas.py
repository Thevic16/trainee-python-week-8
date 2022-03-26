from marshmallow import EXCLUDE

from ma import ma
from models.person_models import PersonModel, RoleModel, FilmPersonRoleModel, \
    ClientModel


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PersonModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE


class FilmPersonRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FilmPersonRoleModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE
        