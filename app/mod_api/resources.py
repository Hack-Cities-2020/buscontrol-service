import json
from flask_restful import Resource, reqparse, marshal_with, abort
from app import db
from app import LOGGER
from app.mod_api.models import *
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

        return AnimalM.query.get_or_404(animal_id)

    @marshal_with(AnimalM.fields)
    def post(self):
        args = self.parser.parse_args()
        animal = AnimalM(**args)
        db.session.add(animal)
        db.session.commit()
        return animal


class Route(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='name of the route')
        self.parser.add_argument('status', type=str, help='route status')
        self.parser.add_argument('path', type=list, location='json')
        self.parser.add_argument('stops', type=list, location='json')
        self.parser.add_argument('checkpoints', type=list, location='json')
        
        self.parser.add_argument('json_path', type=list, location='json')
        # self.parser.add_argument('path', type=list, location='json')

    def get_or_abort(self, route_id):
        if route_id is None:
            abort(404, message='No route id')
            return
        
        route = RouteM.query.get(route_id)
        if route is None:
            abort(404, message=f'Route for id:{route_id} doesn\'t exist')
        
        return route
        
    @marshal_with(RouteM.fields)
    def get(self, route_id=None):
        if route_id is None:
            return RouteM.query.all()
        return self.get_or_abort(route_id)
    
    @marshal_with(RouteM.fields)
    def post(self):
        LOGGER.info('CREATE Route')
        args = self.parser.parse_args()
        stops = [RouteStopM(p['lat'], p['lng']) for p in args['stops']]
        checkpoints = [RouteCheckpointM(p['lat'], p['lng']) for p in args['checkpoints']]
        for p in stops + checkpoints:
            db.session.add(p)

        route = RouteM(args['name'], args['status'])
        route.stops = stops
        route.checkpoints = checkpoints
        
        json_path = json.dumps(args['json_path'])
        route.json_path = json_path
        db.session.add(route)
        db.session.commit()
        # path = json.loads(args['path'])
        return route, 201
  
    @marshal_with(RouteM.fields)
    def put(self, route_id):
        LOGGER.info('UPDATE Route')
        args = self.parser.parse_args()
        stops = []
        checkpoints = []
        if args['stops']: 
            stops = [RouteStopM(p['lat'], p['lng']) for p in args['stops']]
        if args['checkpoints']: 
            checkpoints = [RouteCheckpointM(p['lat'], p['lng']) for p in args['checkpoints']]
        
        route = self.get_or_abort(route_id)

        if args['name']:
            route.name = args['name']
        if args['status']:
            route.status = args['status']
        # if args['path']:
        #     route.path = args['path']
        if stops:
            route.stops = stops
        if checkpoints:
            route.checkpoints = checkpoints
        if args['json_path']:
            route.json_path = json.dumps(args['json_path'])
        
        db.session.commit()
        return route, 201
    
    def delete(self, route_id):
        LOGGER.info('DELETE route')
        route = self.get_or_abort(route_id)
        db.session.delete(route)
        db.session.commit()

        return '', 204

