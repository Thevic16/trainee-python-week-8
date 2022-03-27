from flask import request, make_response, jsonify
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError

from models.models import SeasonModel
from schemas.schemas import SeasonSchema

# Season ----------------------------------------------------------------------
model_name_singular = 'Season'
model_name_plural = 'Seasons'
model = SeasonModel
schema = SeasonSchema()
list_schema = SeasonSchema(many=True)
message_not_found = "Season not found."
namespace = Namespace('seasons',
                      description='Seasons related operations')
model_namespace = namespace.model('Season', {
    'film_id': fields.Integer('Film id of the Season'),
    'title': fields.String('Title of the Season'),
    'season_prequel_id': fields.Integer('Season prequel id of the Season'),
})


class SeasonResource(Resource):
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
            model_data.film_id = model_json['film_id']
            model_data.title = model_json['title']
            model_data.season_prequel_id = model_json['season_prequel_id']
        else:
            model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 200


class SeasonResourceList(Resource):
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
