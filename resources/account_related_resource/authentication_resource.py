from flask import request
from flask_jwt_extended import create_access_token
from flask_restplus import fields, Namespace, Resource
from werkzeug.security import safe_str_cmp

from models.models import AccountModel

# Account ---------------------------------------------------------------------
model_name_singular = 'authentication'
namespace = Namespace(f'{model_name_singular}',
                      description=f'{model_name_singular} related operations')
model_namespace = namespace.model('Authentication', {
    'email': fields.String(f'email of the {model_name_singular}'),
    'password': fields.String(f'password of the {model_name_singular}'),
})


class AuthenticationResource(Resource):
    @namespace.expect(model_namespace)
    @namespace.doc(f'{model_name_singular}')
    def post(self):
        model_json = request.get_json()

        email = model_json['email']
        password = model_json['password']

        account = AccountModel.find_by_email(email)
        if account and safe_str_cmp(account.password, password):
            access_token = create_access_token(
                identity=account.id, fresh=True)
            return {'token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401
