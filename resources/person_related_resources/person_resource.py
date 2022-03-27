from flask import request
from flask_restplus import fields, Namespace, Resource

from models.models import PersonModel
from schemas.schemas import PersonSchema

# Person ---------------------------------------------------------------------
model_name_singular = 'Person'
model_name_plural = 'Persons'
model = PersonModel
schema = PersonSchema()
list_schema = PersonSchema(many=True)
message_not_found = "Person not found."
namespace = Namespace('persons',
                      description='Persons related operations')
model_namespace = namespace.model('Person', {
    'name': fields.String('name of the Person'),
    'lastname': fields.String('lastname of the Person'),
    'gender': fields.String('gender of the Person'),
    'date_of_birth': fields.String('date_of_birth of the Person'),
    'person_type': fields.String('person_type of the Person'),
})


class PersonResource(Resource):
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
            model_data.name = model_json['name']
            model_data.lastname = model_json['lastname']
            model_data.gender = model_json['gender']
            model_data.date_of_birth = model_json['date_of_birth']
            model_data.person_type = model_json['person_type']
        else:
            model_data = schema.load(model_json)

        model_data.save_to_db()
        return schema.dump(model_data), 200


class PersonResourceList(Resource):
    @namespace.doc(f'Get all the {model_name_plural}')
    def get(self):
        return list_schema.dump(model.find_all()), 200

    @namespace.expect(model_namespace)
    @namespace.doc(f'Create an {model_name_singular}')
    def post(self):
        model_json = request.get_json()
        model_data = schema.load(model_json)
        model_data.save_to_db()

        return schema.dump(model_data), 201
