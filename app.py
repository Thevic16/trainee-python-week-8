from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db
from resources.film_resources import (CategoryResource, CategoryResourceList,
                                      category_ns, categories_ns)
from marshmallow import ValidationError

import os
from dotenv import load_dotenv

# Load virtual variables ------------------------------------------------------
load_dotenv()  # take environment variables from .env.

# Initializing Flask app ------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc/', title='Film Rental System Application')
app.register_blueprint(bluePrint)

# Database configuration ------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True

# Add namespaces --------------------------------------------------------------
api.add_namespace(category_ns)
api.add_namespace(categories_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


# Defining resources ----------------------------------------------------------
category_ns.add_resource(CategoryResource, '/<int:id>/')
categories_ns.add_resource(CategoryResourceList, "/")

# Run server ------------------------------------------------------------------
db.init_app(app)
ma.init_app(app)
if os.getenv('DEBUG_STATE') == 'True':
    app.run(port=os.getenv('PORT'), debug=True)
elif os.getenv('DEBUG_STATE') == 'False':
    app.run(port=os.getenv('PORT'), debug=False)