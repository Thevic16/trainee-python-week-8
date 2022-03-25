from marshmallow import EXCLUDE

from ma import ma
from models.film_models import CategoryModel, FilmModel


class CategoryShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        load_instance = True
        include_fk = True


class FilmShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FilmModel
        load_instance = True
        include_fk = True
        unknown = EXCLUDE
