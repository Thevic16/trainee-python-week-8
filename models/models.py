import validators.validators
from db import db
from typing import List

from bussiness_logic.bussiness_logic import FilmBusinessLogic


# Film related models
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
    price_by_day = db.Column(db.Float)
    stock = db.Column(db.Integer)
    film_type = db.Column(db.String(120))
    # Remember add image column

    # One to One relationship
    film_prequel_id = db.Column(db.Integer, db.ForeignKey("film.id"),
                                index=True)

    # Relationship
    category = db.relationship('CategoryModel')
    film_prequel = db.relationship(lambda: FilmModel, remote_side=id,
                                   uselist=False)

    def __init__(self, title, description, release_date, category_id,
                 price_by_day, stock, film_type,
                 film_prequel_id):
        self.title = title
        self.description = description
        self.release_date = release_date
        self.category_id = category_id
        self.price_by_day = price_by_day
        self.stock = stock
        self.availability = 0
        self.film_type = film_type
        self.film_prequel_id = film_prequel_id

    def __repr__(self):
        return self.title

    def json(self):
        return {'title': self.title, 'description': self.description,
                'release_date': self.release_date,
                'category': self.category_id,
                'price_by_day': self.price_by_day, 'stock': self.stock,
                'availability': self.get_availability,
                'film_type': self.film_type}

    @classmethod
    def find_by_id(cls, _id) -> "FilmModel":
        film = cls.query.filter_by(id=_id).first()
        cls.set_availability(film)
        return film

    @classmethod
    def find_all(cls) -> List["FilmModel"]:
        films = cls.query.all()
        for film in films:
            cls.set_availability(film)
        return films

    def save_to_db(self) -> None:
        validators.validators.validator_date_limit_today(self.release_date)
        validators.validators.validator_no_negative(self.price_by_day)
        validators.validators.validator_no_negative(self.stock)
        FilmBusinessLogic.validate_stock_greater_availability(self.stock,
                                                              self.availability
                                                              )
        validators.validators.validate_film_type(self.film_type)

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # Methods
    @staticmethod
    def set_availability(film):
        film.availability = film.stock - \
                            RentModel.get_total_amount_by_film_id(film.id)


class SeasonModel(db.Model):
    __tablename__ = "season"

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))
    title = db.Column(db.String(120), unique=True)
    season_prequel_id = db.Column(db.Integer, db.ForeignKey("season.id"),
                                  index=True)

    # Relationship
    film = db.relationship('FilmModel', uselist=False)
    season_prequel = db.relationship(lambda: SeasonModel, remote_side=id,
                                     uselist=False)

    def __init__(self, film_id, title, season_prequel_id):
        self.film_id = film_id
        self.title = title
        self.season_prequel_id = season_prequel_id

    def __repr__(self):
        return f"{FilmModel.find_by_id(self.film_id).title} - {self.title}"

    def json(self):
        return {'film_id': self.film_id, 'title': self.title,
                'season_prequel_id': self.season_prequel_id}

    @classmethod
    def find_by_id(cls, _id) -> "SeasonModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["SeasonModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class ChapterModel(db.Model):
    __tablename__ = "chapter"

    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    title = db.Column(db.String(120), unique=True)
    chapter_prequel_id = db.Column(db.Integer, db.ForeignKey("chapter.id"),
                                   index=True)

    # Relationship
    season = db.relationship('SeasonModel', uselist=False)
    chapter_prequel = db.relationship(lambda: ChapterModel, remote_side=id,
                                      uselist=False)

    def __init__(self, season_id, title, chapter_prequel_id):
        self.season_id = season_id
        self.title = title
        self.chapter_prequel_id = chapter_prequel_id

    def __repr__(self):
        return f"{SeasonModel.find_by_id(self.season_id).title} - {self.title}"

    def json(self):
        return {'season_id': self.season_id, 'title': self.title,
                'chapter_prequel_id': self.chapter_prequel_id}

    @classmethod
    def find_by_id(cls, _id) -> "ChapterModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ChapterModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


# Person related models
class PersonModel(db.Model):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    date_of_birth = db.Column(db.Date)
    person_type = db.Column(db.String(120))

    def __init__(self, name, lastname, gender, date_of_birth, person_type):
        self.name = name
        self.lastname = lastname
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.person_type = person_type

    def __repr__(self):
        return f"{self.name} {self.lastname}"

    def json(self):
        return {'name': self.name, 'lastname': self.lastname,
                'gender': self.gender, 'date_of_birth': self.date_of_birth,
                'person_type': self.person_type}

    @classmethod
    def find_by_name(cls, name) -> "PersonModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "PersonModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["PersonModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class RoleModel(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name

    def json(self):
        return {'name': self.name, 'description': self.description}

    @classmethod
    def find_by_name(cls, name) -> "RoleModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "RoleModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["RoleModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class FilmPersonRoleModel(db.Model):
    __tablename__ = "filmpersonrole"

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # Relationship
    film = db.relationship('FilmModel')
    person = db.relationship('PersonModel')
    role = db.relationship('RoleModel')

    def __init__(self, film_id, person_id, role_id):
        self.film_id = film_id
        self.person_id = person_id
        self.role_id = role_id

    def __repr__(self):
        return f"{RoleModel.find_by_id(self.role_id).name} - " \
               f"{FilmModel.find_by_id(self.film_id).title} - " \
               f"{PersonModel.find_by_id(self.person_id).name} - " \
               f"{PersonModel.find_by_id(self.person_id).lastname}"

    def json(self):
        return {'film_id': self.film_id, 'person_id': self.person_id,
                'role_id': self.role_id}

    @classmethod
    def find_by_id(cls, _id) -> "FilmPersonRole":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["FilmPersonRole"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class ClientModel(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    direction = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(120))
    email = db.Column(db.String(120))

    # Relationship
    person = db.relationship('PersonModel', uselist=False)

    def __init__(self, person_id, direction, phone, email):
        self.person_id = person_id
        self.direction = direction
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"{PersonModel.find_by_id(self.person_id).name} - " \
               f"{PersonModel.find_by_id(self.person_id).lastname}"

    def json(self):
        return {'person_id': self.person_id, 'direction': self.direction,
                'phone': self.phone, 'email': self.email}

    @classmethod
    def find_by_id(cls, _id) -> "Client":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Client"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        validators.validate_email(self.email)
        validators.validate_phone(self.phone)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


# Rent related model
class RentModel(db.Model):
    __tablename__ = "rent"

    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    amount = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    actual_return_date = db.Column(db.Date, nullable=True)
    state = db.Column(db.String(120))

    # Relationship
    film = db.relationship('FilmModel')
    client = db.relationship('ClientModel')

    def __init__(self, film_id, client_id, amount, start_date, return_date,
                 actual_return_date, state):
        self.film_id = film_id
        self.client_id = client_id
        self.amount = amount
        self.start_date = start_date
        self.return_date = return_date
        self.actual_return_date = actual_return_date
        self.state = state

    def __repr__(self):
        return \
            f"{FilmModel.find_by_id(self.film_id)} - " \
            f"{self.get_client_full_name()} -" \
            f"{self.return_date} "

    def json(self):
        return {'film_id': self.film_id, 'client_id': self.client_id,
                'amount': self.amount, 'start_date': self.start_date,
                'return_date': self.return_date,
                'actual_return_date': self.actual_return_date,
                'state': self.state}

    @classmethod
    def find_by_id(cls, _id) -> "RentModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["RentModel"]:
        return cls.query.all()

    @classmethod
    def find_all_count_by_film_id(cls, film_id: int) -> List["RentModel"]:
        return cls.query.filter_by(film_id=film_id).count()

    @classmethod
    def find_all_by_film_id(cls, film_id: int) -> List["RentModel"]:
        return cls.query.filter_by(film_id=film_id)

    @classmethod
    def get_total_amount_by_film_id(cls, film_id: int) -> int:
        total = 0
        for film in cls.find_all_by_film_id(film_id):
            total += film.amount
        return total

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # Methods
    def get_client_full_name(self):
        return f"{PersonModel.find_by_id(self.get_person_id()).name} -" \
               f"{PersonModel.find_by_id(self.get_person_id()).lastname}"

    def get_person_id(self):
        return ClientModel.find_by_id(self.film_id).person_id
