from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from flask_migrate import Migrate

from ma import ma
from db import db
from resources.film_related_resources import category_resource
from resources.film_related_resources import film_resource
from resources.film_related_resources import season_resource
from resources.film_related_resources import chapter_resource

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
# Film app
api.add_namespace(category_resource.namespace)
api.add_namespace(film_resource.namespace)
api.add_namespace(season_resource.namespace)
api.add_namespace(chapter_resource.namespace)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


# Defining resources ----------------------------------------------------------
# Film app
category_resource.namespace.add_resource(category_resource.CategoryResource,
                                         '/<int:id>/')
category_resource.namespace.add_resource(
    category_resource.CategoryResourceList, "/")

film_resource.namespace.add_resource(film_resource.FilmResource, '/<int:id>/')
film_resource.namespace.add_resource(film_resource.FilmResourceList, "/")

season_resource.namespace.add_resource(season_resource.SeasonResource,
                                       '/<int:id>/')
season_resource.namespace.add_resource(season_resource.SeasonResourceList,
                                       "/")

chapter_resource.namespace.add_resource(chapter_resource.ChapterResource,
                                        '/<int:id>/')
chapter_resource.namespace.add_resource(chapter_resource.ChapterResourceList,
                                        "/")

# Run server ------------------------------------------------------------------
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)  # Add migrations

if os.getenv('DEBUG_STATE') == 'True':
    app.run(port=os.getenv('PORT'), debug=True)
elif os.getenv('DEBUG_STATE') == 'False':
    app.run(port=os.getenv('PORT'), debug=False)
