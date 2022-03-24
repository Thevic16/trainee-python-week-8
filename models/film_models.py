from db import db
from typing import List


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name

    def json(self):
        return {'name': self.name, 'description': self.description}

    @classmethod
    def find_by_name(cls, name) -> "CategoryModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "CategoryModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


'''
class FilmModel(db.Model):
    __tablename__ = "film"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime)
    
    category = db.relationship(
        'CategoryModel', backref=db.backref('films', lazy='dynamic')
    )
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    price_by_day = db.Column(db.Float)
    stock = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    film_type = db.Column(db.String(120))
    # Remember add image column

    # One to One relationship

        #   film_prequel = db.relationship(
        #   'Film', uselist=False
        #   )
    

    def __repr__(self):
        return self.title
'''