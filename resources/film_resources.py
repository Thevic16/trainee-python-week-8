from flask import request
from flask_restplus import Resource, fields, Namespace

from models.film_models import CategoryModel
from schemas.film_schemas import CategoryShema

CATEGORY_NOT_FOUND = "Category not found."

category_ns = Namespace('categories', description='Category related operations')
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
            return CategoryModel.dump(category_data)
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
