from flask import request
from flask_restplus import fields, Namespace, Resource

from models.film_models import ChapterModel
from schemas.film_schemas import ChapterSchema

# Chapter ---------------------------------------------------------------------
model_name_singular = 'Chapter'
model_name_plural = 'Chapters'
model = ChapterModel
schema = ChapterSchema()
list_schema = ChapterSchema(many=True)
message_not_found = "Chapter not found."
namespace = Namespace('chapters',
                      description='chapters related operations')
model_namespace = namespace.model('Chapter', {
    'season_id': fields.Integer('Season id of the Season'),
    'title': fields.String('Title of the Season'),
    'chapter_prequel_id': fields.Integer('Chapter prequel id of the Chapter'),
})


class ChapterResource(Resource):
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
            model_data.season_id = model_json['season_id']
            model_data.title = model_json['title']
            model_data.chapter_prequel_id = model_json['chapter_prequel_id']
        else:
            model_data = schema.load(model_json)

        model_data.save_to_db()
        return schema.dump(model_data), 200


class ChapterResourceList(Resource):
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
