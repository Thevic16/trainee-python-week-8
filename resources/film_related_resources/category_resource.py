from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restplus import fields, Namespace, Resource
from marshmallow import ValidationError

from models.models import CategoryModel
from schemas.schemas import CategorySchema

# Category --------------------------------------------------------------------
model_name_singular = 'Category'
model_name_plural = 'Categories'
model = CategoryModel
schema = CategorySchema()
list_schema = CategorySchema(many=True)
message_not_found = "Category not found."
namespace = Namespace('categories',
                      description='Categories related operations')
model_namespace = namespace.model('Category', {
    'name': fields.String('Name of the Category'),
    'description': fields.String('Description of the Category')
})


class CategoryResource(Resource):
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


class CategoryResourceList(Resource):
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
