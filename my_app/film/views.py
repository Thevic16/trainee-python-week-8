from flask import request, jsonify, Blueprint
from my_app import db
from my_app.film.models import Category, Film

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


@film.route('/api/films/', methods=['GET', 'POST'])
def films():
    if request.method == 'GET':
        films = Film.query.all()
        res = {}
        for film in films:
            res[film.id] = {
                'title': film.title,
                'description': film.description,
                'release_date': film.release_date,
                'category': film.category.id,
                'price_by_day': film.price_by_day,
                'stock': film.stock,
                'availability': film.availability,
                'film_type': film.film_type
                # 'film_prequel': film.film_prequel.title
            }
        return jsonify(res)
    elif request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        release_date = request.form.get('release_date')
        category_id = int(request.form.get('category_id'))
        price_by_day = request.form.get('price_by_day')
        stock = request.form.get('stock')
        availability = request.form.get('availability')
        film_type = request.form.get('film_type')
        # film_prequel = request.form.get('film_prequel')

        category = Category.query.get_or_404(category_id)

        film = Film(title=title, description=description,
                    release_date=release_date, category_id=category_id,
                    category=category, price_by_day=price_by_day,
                    stock=stock, availability=availability,
                    film_type=film_type)
        # film_prequel=film_prequel)

        db.session.add(film)
        db.session.commit()
        return f'film create: film: {film}'
