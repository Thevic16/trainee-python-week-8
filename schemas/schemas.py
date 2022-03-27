from marshmallow import EXCLUDE
from ma import ma
from models.models import CategoryModel, FilmModel, SeasonModel, ChapterModel, \
    PersonModel, RoleModel, FilmPersonRoleModel, ClientModel, RentModel
from marshmallow import fields


# Film related schemas
class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        load_instance = True
        include_fk = True


class FilmSchema(ma.SQLAlchemyAutoSchema):
    availability = fields.Integer()

    class Meta:
        model = FilmModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE


class SeasonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SeasonModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE


class ChapterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChapterModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE


# Person related schemas
class PersonSchema(ma.SQLAlchemyAutoSchema):
    age = fields.Integer()

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


# Rent related schemas
class RentSchema(ma.SQLAlchemyAutoSchema):
    cost = fields.Float()

    class Meta:
        model = RentModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE
