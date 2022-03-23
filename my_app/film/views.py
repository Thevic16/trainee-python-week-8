from flask import request, jsonify, Blueprint
from my_app import db
from my_app.film.models import Category

film = Blueprint('film', __name__)


@film.route('/')
@film.route('/home')
def home():
    return "Welcome to the Film Home."


'''
@film.route('/api/categories/<id>')
def categories(id):
    category = Category.query.get_or_404(id)
    return f'Category - name:{category.name},' \
           f' description:{category.description}'
'''


@film.route('/api/categories/', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        categories = Category.query.all()
        res = {}
        for category in categories:
            res[category.id] = {
                'name': category.name,
                'description': category.description
            }
        return jsonify(res)
    elif request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        return f'Category create: category: {category}'
