from db import db
from typing import List

from models.film_models import FilmModel
from models.person_models import ClientModel, PersonModel


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
