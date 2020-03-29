from app import db
from app.mod_test.models import AnimalM
from flask_restful import Resource, reqparse, fields, marshal_with


class Animal(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='name of the animal')
        self.parser.add_argument('species', type=str, help='species of the animal')
        self.parser.add_argument('greeting', type=str, help='greeting of the animal')
        
    @marshal_with(AnimalM.fields, envelope='animal')
    def get(self, id):
        animal = AnimalM.query.filter_by(id=id).first()
        return animal
    
    def post(self):
        args = self.parser.parse_args()
        animal = AnimalM(**args)
        db.session.add(animal)
        return {'animal':'create'}