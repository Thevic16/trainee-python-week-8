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
    def find_all(cls) -> List["CategoryModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class FilmModel(db.Model):
    __tablename__ = "film"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(
        'CategoryModel', backref=db.backref('films', lazy='dynamic')
    )

    price_by_day = db.Column(db.Float)
    stock = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    film_type = db.Column(db.String(120))

    # Remember add image column

    # One to One relationship
    film_prequel_id = db.Column(db.Integer, db.ForeignKey("film.id"),
                                index=True)
    film_prequel = db.relationship(lambda: FilmModel, remote_side=id,
                                   uselist=False)

    def __init__(self, title, description, release_date, category_id,
                 price_by_day, stock, availability, film_type,
                 film_prequel_id):
        self.title = title
        self.description = description
        self.release_date = release_date
        self.category_id = category_id
        self.price_by_day = price_by_day
        self.stock = stock
        self.availability = availability
        self.film_type = film_type
        self.film_prequel_id = film_prequel_id

    def __repr__(self):
        return self.title

    def json(self):
        return {'title': self.title, 'description': self.description,
                'release_date': self.release_date, 'category': self.category_id
            , 'price_by_day': self.price_by_day, 'stock': self.stock,
                'availability': self.availability, 'film_type': self.film_type}

    @classmethod
    def find_by_id(cls, _id) -> "FilmModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["FilmModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
