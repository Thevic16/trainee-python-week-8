from my_app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.name


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(
        'Category', backref=db.backref('films', lazy='dynamic')
    )
    price_by_day = db.Column(db.Float)
    stock = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    film_type = db.Column(db.String(120))
    # Remember add image column

    # One to One relationship
    '''
        film_prequel = db.relationship(
        'Film', uselist=False
        )
    '''

    def __repr__(self):
        return self.title
