from ma import ma
from models.film_models import CategoryModel


class CategoryShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel
        load_instance = True
        include_fk = True
