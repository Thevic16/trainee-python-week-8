from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_claims, jwt_required
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError
from datetime import datetime

from models.models import RentModel
from schemas.schemas import RentSchema

# Rent ------------------------------------------------------------------------
model_name_singular = 'rent'
model_name_plural = 'rents'
model = RentModel
schema = RentSchema()
list_schema = RentSchema(many=True)
message_not_found = f"{model_name_singular} not found."
namespace = Namespace(f'{model_name_plural}',
                      description=f'{model_name_plural} related operations')
model_namespace = namespace.model('Rent', {
    'film_id': fields.Integer(f'film_id of the {model_name_singular}'),
    'client_id': fields.Integer(f'client_id of the {model_name_singular}'),
    'amount': fields.Integer(f'amount of the {model_name_singular}'),
    'start_date': fields.String(f'start_date of the {model_name_singular}'),
    'return_date': fields.String(f'return_date of the {model_name_singular}'),
    'actual_return_date':
        fields.String(f'actual_return_date of the {model_name_singular}'),
    'state': fields.String(f'state of the {model_name_singular}'),
})


class RentResource(Resource):
    def get(self, id):
        model_data = model.find_by_id(id)
        if model_data:
            return schema.dump(model_data)
        return {'message': message_not_found}, 404

    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()

        if not claims['is_admin'] and not claims['is_employee']:
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

        if not claims['is_admin'] and not claims['is_employee']:
            return {'message': 'Admin privilege required.'}, 401

        model_data = model.find_by_id(id)
        model_json = request.get_json()

        if model_data:
            model_data.film_id = model_json['film_id']
            model_data.client_id = model_json['client_id']
            model_data.amount = model_json['amount']
            model_data.start_date = datetime.strptime(model_json['start_date'],
                                                      '%Y-%m-%d').date()
            model_data.return_date = datetime.strptime(
                model_json['return_date']
                , '%Y-%m-%d').date()
            model_data.actual_return_date = datetime.strptime(
                model_json['actual_return_date']
                , '%Y-%m-%d').date()
            model_data.state = model_json['state']
        else:
            model_data = schema.load(model_json)

        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 200


class RentResourceList(Resource):
    @namespace.doc(f'Get all the {model_name_plural}')
    def get(self):
        return list_schema.dump(model.find_all()), 200

    @jwt_required
    @namespace.expect(model_namespace)
    @namespace.doc(f'Create an {model_name_singular}')
    def post(self):
        claims = get_jwt_claims()

        if not claims['is_admin'] and not claims['is_employee']:
            return {'message': 'Admin privilege required.'}, 401

        model_json = request.get_json()
        model_data = schema.load(model_json)
        try:
            model_data.save_to_db()
        except ValidationError as err:
            return make_response(jsonify(msg=f'Error: {err.messages}. '), 400)

        return schema.dump(model_data), 201
