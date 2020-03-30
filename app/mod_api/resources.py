import json
from flask_restful import Resource, reqparse, marshal_with, abort
import sqlalchemy.exc as sql_exception
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
        self.parser.add_argument('path_color', type=str, help='route path color')
        self.parser.add_argument('path', type=list, location='json')
        self.parser.add_argument('stops', type=list, location='json')
        self.parser.add_argument('checkpoints', type=list, location='json')
        
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
        stops = []
        checkpoints = []
        if args['stops']: 
            stops = [RouteStopM(p['lat'], p['lng']) for p in args['stops']]
        if args['checkpoints']: 
            checkpoints = [RouteCheckpointM(p['lat'], p['lng']) for p in args['checkpoints']]
        
        for p in stops + checkpoints:
            db.session.add(p)

        route = RouteM(args['name'], args['status'])
        
        if args['path_color']:
            route.path_color = args['path_color']
        if args['path']:
            route.path = json.dumps(args['path'])
        if stops:
            route.stops = stops
        if checkpoints:
            route.checkpoints = checkpoints

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
        if args['path_color']:
            route.path_color = args['path_color']
        if args['path']:
            route.path = json.dumps(args['path'])
        if stops:
            route.stops = stops
        if checkpoints:
            route.checkpoints = checkpoints
        
        db.session.commit()
        return route, 201
    
    def delete(self, route_id):
        LOGGER.info('DELETE route')
        route = self.get_or_abort(route_id)
        db.session.delete(route)
        db.session.commit()

        return '', 204


class Vehicle(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('plate', type=str, help='vehicle plate is required')
        self.parser.add_argument('model', type=str, help='model of the vehicle')
        self.parser.add_argument('year', type=int, help='year of the vehicle')
        self.parser.add_argument('manufacturer', type=str, help='manufacturer of the vehicle')
        self.parser.add_argument('capacity', type=str, help='capacity of the vehicle')        
        self.parser.add_argument('driver', type=dict, help='driver information missing!')
        self.parser_post = self.parser.copy()
        self.parser_post.add_argument('route_id', required=True,type=int, help='route_id is required!')

    def get_or_abort(self, vehicle_id):
        if vehicle_id is None:
            abort(404, message='No vehicle id')
            return
        
        vehicle = VehicleM.query.get(vehicle_id)
        if vehicle is None:
            abort(404, message=f'Vehicle for id:{vehicle_id} doesn\'t exist')
        
        return vehicle

    @marshal_with(VehicleM.fields)
    def get(self, vehicle_id=None):
        if vehicle_id is None:
            return VehicleM.query.all()

        return self.get_or_abort(vehicle_id)
    
    @marshal_with(VehicleM.fields)
    def post(self):
        LOGGER.info('CREATE Vehicle')
        args = self.parser_post.parse_args()
        driver_dic = args['driver']
        driver = DriverM(**driver_dic)
        db.session.add(driver)
        LOGGER.debug(f'driver: {driver}')

        vehicle = VehicleM(args['plate'])
        vehicle.driver = driver
        if args['model']:
            vehicle.model = args['model']
        if args['year']:
            vehicle.year = args['year']
        if args['manufacturer']:
            vehicle.manufacturer = args['manufacturer']
        if args['capacity']:
            vehicle.capacity = args['capacity']
        if args['route_id']:
            vehicle.route_id = args['route_id']

        db.session.add(vehicle)
        # agregar vehicle a ruta
        route = RouteM.query.get(vehicle.route_id)
        route.vehicles.append(vehicle)
        LOGGER.debug(f'route: {route}')
        try:
            db.session.commit()
        except sql_exception.IntegrityError as e:
            abort(403, message='duplicate plates not allowed')
        # path = json.loads(args['path'])
        return vehicle, 201

    @marshal_with(VehicleM.fields)
    def put(self):
        LOGGER.info('UPDATE Vehicle')
        args = self.parser_post.parse_args()
        driver_dic = args['driver']
        driver = DriverM(**driver_dic)
        db.session.add(driver)
        LOGGER.debug(f'driver: {driver}')

        vehicle = VehicleM(args['plate'])
        vehicle.driver = driver
        if args['model']:
            vehicle.model = args['model']
        if args['year']:
            vehicle.year = args['year']
        if args['manufacturer']:
            vehicle.manufacturer = args['manufacturer']
        if args['capacity']:
            vehicle.capacity = args['capacity']
        if args['route_id']:
            vehicle.route_id = args['route_id']

        db.session.add(vehicle)
        db.session.commit()
        return vehicle, 201

    def delete(self, vehicle_id):
        LOGGER.info('DELETE vehicle')
        vehicle = self.get_or_abort(vehicle_id)
        db.session.delete(vehicle)
        db.session.commit()

        return '', 204