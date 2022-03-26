from db import db
from typing import List

from models.film_models import FilmModel


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
    def find_by_name(cls, name) -> "FilmPersonRole":
        return cls.query.filter_by(name=name).first()

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
    def find_by_name(cls, name) -> "Client":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "Client":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Client"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
