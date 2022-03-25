from datetime import datetime
from flask import request
from flask_restplus import Resource, fields, Namespace

from models.film_models import CategoryModel, FilmModel
from schemas.film_schemas import CategoryShema, FilmShema

# Category --------------------------------------------------------------------
CATEGORY_NOT_FOUND = "Category not found."

category_ns = Namespace('categories',
                        description='Category related operations')
categories_ns = Namespace('categories',
                          description='Categories related operations')

category_schema = CategoryShema()
category_list_schema = CategoryShema(many=True)

# Model required by flask_restplus for expect
category = categories_ns.model('Category', {
    'name': fields.String('Name of the Category'),
    'description': fields.String('Description of the Category')
})


class CategoryResource(Resource):

    def get(self, id):
        category_data = CategoryModel.find_by_id(id)
        if category_data:
            return category_schema.dump(category_data)
        return {'message': CATEGORY_NOT_FOUND}, 404

    def delete(self, id):
        category_data = CategoryModel.find_by_id(id)
        if category_data:
            category_data.delete_from_db()
            return {'message': "Category Deleted successfully"}, 200
        return {'message': CATEGORY_NOT_FOUND}, 404

    @category_ns.expect(category)
    def put(self, id):
        category_data = CategoryModel.find_by_id(id)
        category_json = request.get_json()

        if category_data:
            category_data.name = category_json['name']
            category_data.description = category_json['description']
        else:
            category_data = category_schema.load(category_json)

        category_data.save_to_db()
        return category_schema.dump(category_data), 200


class CategoryResourceList(Resource):
    @categories_ns.doc('Get all the Categories')
    def get(self):
        return category_list_schema.dump(CategoryModel.find_all()), 200

    @categories_ns.expect(category)
    @categories_ns.doc('Create an Category')
    def post(self):
        category_json = request.get_json()
        categoty_data = category_schema.load(category_json)
        categoty_data.save_to_db()

        return category_schema.dump(categoty_data), 201


# Film ------------------------------------------------------------------------

FILM_NOT_FOUND = "Film not found."

film_ns = Namespace('films',
                    description='Film related operations')
films_ns = Namespace('films',
                     description='Films related operations')

film_schema = FilmShema()
film_list_schema = FilmShema(many=True)

# Model required by flask_restplus for expect
film = films_ns.model('Film', {
    'title': fields.String('Title of the Film'),
    'description': fields.String('Description of the Film'),
    'release_date': fields.Date(),
    'category_id': fields.Integer('Category of the Film'),
    'price_by_day': fields.Float('Price by day of the Film'),
    'stock': fields.Integer('Stock of the Film'),
    'availability': fields.Integer('Availability of the Film'),
    'film_type': fields.String('Film type of the Film'),
    'film_prequel_id': fields.Integer('Film prequel of the Film'),
})


class FilmResource(Resource):

    def get(self, id):
        film_data = FilmModel.find_by_id(id)
        if film_data:
            return film_schema.dump(film_data)
        return {'message': FILM_NOT_FOUND}, 404

    def delete(self, id):
        film_data = FilmModel.find_by_id(id)
        if film_data:
            film_data.delete_from_db()
            return {'message': "Film Deleted successfully"}, 200
        return {'message': FILM_NOT_FOUND}, 404

    @film_ns.expect(film)
    def put(self, id):
        film_data = FilmModel.find_by_id(id)
        film_json = request.get_json()

        if film_data:
            film_data.title = film_json['title']
            film_data.description = film_json['description']
            film_data.release_date = datetime.strptime(
                film_json['release_date'], '%Y-%m-%d').date()
            film_data.category_id = film_json['category_id']
            film_data.stock = film_json['stock']
            film_data.availability = film_json['availability']
            film_data.film_type = film_json['film_type']
            film_data.film_prequel_id = film_json['film_prequel_id']

        else:
            film_data = film_schema.load(film_json)

        film_data.save_to_db()
        return film_schema.dump(film_data), 200


class FilmResourceList(Resource):
    @films_ns.doc('Get all the Films')
    def get(self):
        return film_list_schema.dump(FilmModel.find_all()), 200

    @film_ns.expect(film)
    @film_ns.doc('Create an Film')
    def post(self):
        film_json = request.get_json()
        film_data = film_schema.load(film_json)
        film_data.save_to_db()

        return film_schema.dump(film_data), 201
