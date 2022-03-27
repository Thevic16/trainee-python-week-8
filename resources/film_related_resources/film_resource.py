from datetime import datetime
from flask import request, jsonify, make_response
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError

from models.models import FilmModel
from schemas.schemas import FilmSchema

model_name_singular = 'Film'
model_name_plural = 'Films'
model = FilmModel
schema = FilmSchema()
list_schema = FilmSchema(many=True)
message_not_found = "Film not found."
namespace = Namespace('films',
                      description='Films related operations')

model_namespace = namespace.model('Film', {
    'title': fields.String('Title of the Film'),
    'description': fields.String('Description of the Film'),
    'release_date': fields.Date(),
    'category_id': fields.Integer('Category of the Film'),
    'price_by_day': fields.Float('Price by day of the Film'),
    'stock': fields.Integer('Stock of the Film'),
    # 'availability': fields.Integer('Availability of the Film'),
    'film_type': fields.String('Film type of the Film'),
    'film_prequel_id': fields.Integer('Film prequel of the Film'),
})


class FilmResource(Resource):

    def get(self, id):
        model_data = model.find_by_id(id)
        if model_data:
            return schema.dump(model_data)
        return {'message': message_not_found}, 404

    def delete(self, id):
        model_data = model.find_by_id(id)
        if model_data:
            model_data.delete_from_db()
            return {'message': f"{model_name_singular}"
                               f" Deleted successfully"}, 200
        return {'message': message_not_found}, 404

    @namespace.expect(model_namespace)
    def put(self, id):
        model_data = model.find_by_id(id)
        model_json = request.get_json()

        if model_data:
            model_data.title = model_json['title']
            model_data.description = model_json['description']
            model_data.release_date = datetime.strptime(
                model_json['release_date'], '%Y-%m-%d').date()
            model_data.category_id = model_json['category_id']
            model_data.stock = model_json['stock']
            model_data.film_type = model_json['film_type']
            model_data.film_prequel_id = model_json['film_prequel_id']
        else:
            model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 200


class FilmResourceList(Resource):
    @namespace.doc(f'Get all the {model_name_plural}')
    def get(self):
        return list_schema.dump(model.find_all()), 200

    @namespace.expect(model_namespace)
    @namespace.doc(f'Create an {model_name_singular}')
    def post(self):
        model_json = request.get_json()
        model_data = schema.load(model_json)
        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 201
