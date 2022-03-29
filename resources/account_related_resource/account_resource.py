from flask import request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError

from models.models import AccountModel
from schemas.schemas import AccountSchema

# Account ---------------------------------------------------------------------
model_name_singular = 'account'
model_name_plural = 'accounts'
model = AccountModel
schema = AccountSchema()
list_schema = AccountSchema(many=True)
message_not_found = f"{model_name_singular} not found."
namespace = Namespace(f'{model_name_plural}',
                      description=f'{model_name_plural} related operations')
model_namespace = namespace.model('Account', {
    'email': fields.String(f'email of the {model_name_singular}'),
    'password': fields.String(f'password of the {model_name_singular}'),
    'is_admin': fields.Boolean(f'password of the {model_name_singular}'),
    'is_employee': fields.Boolean(f'password of the {model_name_singular}'),
})


class AccountResource(Resource):
    @jwt_required
    def get(self, id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

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
            model_data.email = model_json['email']
            model_data.password = model_json['password']
            model_data.is_admin = model_json['is_admin']
            model_data.is_employee = model_json['is_employee']
        else:
            model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 200


class AccountResourceList(Resource):
    @jwt_required
    @namespace.doc(f'Get all the {model_name_plural}')
    def get(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

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
