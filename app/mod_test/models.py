from flask_restful import fields
from app import db
from app.models import Base

# Define a Animal model
class AnimalM(Base):
    __tablename__ = 'test_animal'

    name = db.Column(db.String(128), nullable=False)
    species = db.Column(db.String(128), nullable=False)
    greeting = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(256), nullable=False)

    #output fields
    fields = {
        'id': fields.Integer,
        'name': fields.String,
        'species': fields.String,
        'greeting': fields.String
    }

    def __init__(self, name, species, greeting):
        self.name = name
        self.species = species
        self.greeting = greeting
        self.status = 1

    def __repr__(self):
        return f'<Animal {self.species}:{self.name}>'
