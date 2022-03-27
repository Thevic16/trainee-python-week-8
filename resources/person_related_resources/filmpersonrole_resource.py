from flask import request, make_response, jsonify
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError

from models.models import FilmPersonRoleModel
from schemas.schemas import FilmPersonRoleSchema

# FilmPersonRole --------------------------------------------------------------
model_name_singular = 'film_person_role'
model_name_plural = 'films_persons_roles'
model = FilmPersonRoleModel
schema = FilmPersonRoleSchema()
list_schema = FilmPersonRoleSchema(many=True)
message_not_found = f"{model_name_singular} not found."
namespace = Namespace(f'{model_name_plural}',
                      description=f'{model_name_plural} related operations')
model_namespace = namespace.model('FilmPersonRole', {
    'film_id': fields.Integer(f'film_id of the {model_name_singular}'),
    'person_id': fields.Integer(f'person_id of the {model_name_singular}'),
    'role_id': fields.Integer(f'role_id of the {model_name_singular}'),
})


class FilmPersonRoleResource(Resource):
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
            model_data.person_id = model_json['person_id']
            model_data.role_id = model_json['role_id']
        else:
            model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 200


class FilmPersonRoleResourceList(Resource):
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
