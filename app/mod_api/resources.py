from flask_restful import Resource, reqparse, marshal_with
from app import db
from app.mod_test.models import AnimalM


class Animal(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='name of the animal')
        self.parser.add_argument('species', type=str, help='species of the animal')
        self.parser.add_argument('greeting', type=str, help='greeting of the animal')

    @marshal_with(AnimalM.fields)
    def get(self, animal_id=None):
        if animal_id is None:
            return AnimalM.query.all()

        return AnimalM.query.get(animal_id)

    @marshal_with(AnimalM.fields)
    def post(self):
        args = self.parser.parse_args()
        animal = AnimalM(**args)
        db.session.add(animal)
        db.session.commit()
        return animal
