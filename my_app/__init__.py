import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

# Database and ORM configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

from my_app.film.views import film
app.register_blueprint(film)

db.create_all()
