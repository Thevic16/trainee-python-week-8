from flask import request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError

from models.models import RoleModel
from schemas.schemas import RoleSchema

# role ---------------------------------------------------------------------
model_name_singular = 'role'
model_name_plural = 'roles'
model = RoleModel
schema = RoleSchema()
list_schema = RoleSchema(many=True)
message_not_found = f"{model_name_singular} not found."
namespace = Namespace(f'{model_name_plural}',
                      description=f'{model_name_plural} related operations')
model_namespace = namespace.model('Role', {
    'name': fields.String(f'name of the {model_name_singular}'),
    'description': fields.String(f'description of the {model_name_singular}'),
})


class RoleResource(Resource):
    def get(self, id):
        model_data = model.find_by_id(id)
        if model_data:
            return schema.dump(model_data)
        return {'message': message_not_found}, 404

    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        model_data = model.find_by_id(id)
        if model_data:
            model_data.delete_from_db()
            return {'message': f"{model_name_singular}"
                               f" Deleted successfully"}, 200
        return {'message': message_not_found}, 404

    @jwt_required
    @namespace.expect(model_namespace)
    def put(self, id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        model_data = model.find_by_id(id)
        model_json = request.get_json()

        if model_data:
            model_data.name = model_json['name']
            model_data.description = model_json['description']
        else:
            model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 200


class RoleResourceList(Resource):
    @namespace.doc(f'Get all the {model_name_plural}')
    def get(self):
        return list_schema.dump(model.find_all()), 200

    @jwt_required
    @namespace.expect(model_namespace)
    @namespace.doc(f'Create an {model_name_singular}')
    def post(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        model_json = request.get_json()
        model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 201
