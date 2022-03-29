from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_claims, jwt_required
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError

from models.models import ClientModel
from schemas.schemas import ClientSchema

# Client ---------------------------------------------------------------------

model_name_singular = 'client'
model_name_plural = 'clients'
model = ClientModel
schema = ClientSchema()
list_schema = ClientSchema(many=True)
message_not_found = f"{model_name_singular} not found."
namespace = Namespace(f'{model_name_plural}',
                      description=f'{model_name_plural} related operations')
model_namespace = namespace.model('Client', {
    'person_id': fields.Integer(f'person_id of the {model_name_singular}'),
    'direction': fields.String(f'direction of the {model_name_singular}'),
    'phone': fields.String(f'phone of the {model_name_singular}'),
    'email': fields.String(f'email of the {model_name_singular}'),
})


class ClientResource(Resource):
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
            model_data.person_id = model_json['person_id']
            model_data.direction = model_json['direction']
            model_data.phone = model_json['phone']
            model_data.email = model_json['email']
        else:
            model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 200


class ClientResourceList(Resource):
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
