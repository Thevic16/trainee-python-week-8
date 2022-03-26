from marshmallow import EXCLUDE

from ma import ma
from models.film_models import (CategoryModel, FilmModel, SeasonModel,
                                ChapterModel)


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        load_instance = True
        include_fk = True


class FilmSchema(ma.SQLAlchemyAutoSchema):
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
