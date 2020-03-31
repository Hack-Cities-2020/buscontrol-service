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
            stops = [RouteStopM(**p) for p in args['stops']]
        if args['checkpoints']: 
            checkpoints = [RouteCheckpointM(**p) for p in args['checkpoints']]
        
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
        return route, 200
    
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
        vehicle = VehicleM(args['plate'])
        LOGGER.debug(f'vehicle: {vehicle}')

        driver_dic = args['driver']
        if driver_dic is not None:
            driver = DriverM(**driver_dic)
            db.session.add(driver)
            LOGGER.debug(f'driver: {driver}')

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

        # agregar vehicle a ruta
        try:
            route = RouteM.query.get(vehicle.route_id)
            if route is None:
                abort(404, message='route_id not found')
            LOGGER.debug(f'route: {route}')
            route.vehicles.append(vehicle)
            db.session.add(vehicle)
            db.session.commit()
        except sql_exception.IntegrityError as e:
            abort(403, message='duplicate plates not allowed')
        # path = json.loads(args['path'])
        return vehicle, 201

    @marshal_with(VehicleM.fields)
    def put(self, vehicle_id):
        LOGGER.info('UPDATE Vehicle')
        args = self.parser.parse_args()
        vehicle = self.get_or_abort(vehicle_id)

        driver_dic = args['driver']
        LOGGER.debug(driver_dic)
        if driver_dic is not None:  # si llega info de un driver
            if vehicle.driver is not None: # si ya hay un driver
                if vehicle.driver.id == driver_dic.get('id', None): # si es el mismo driver
                    # existente
                    vehicle.driver.full_name = driver_dic.get('full_name', vehicle.driver.full_name)
                    vehicle.driver.ci = driver_dic.get('ci', vehicle.driver.ci)
                else:
                    if driver_dic.get('id', None) is not None:            
                        db.session.delete(vehicle.driver)
                    driver = DriverM(**driver_dic)
                    db.session.add(driver)
                    vehicle.driver = driver
                    LOGGER.debug(f'updated driver: {driver}')
            else:
                driver = DriverM(**driver_dic)
                db.session.add(driver)
                vehicle.driver = driver
                LOGGER.debug(f'new driver: {driver}')

        if args['model']:
            vehicle.model = args['model']
        if args['year']:
            vehicle.year = args['year']
        if args['manufacturer']:
            vehicle.manufacturer = args['manufacturer']
        if args['capacity']:
            vehicle.capacity = args['capacity']
        if args.get('route_id', None):
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

class RouteStops(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('stops', type=list, required=True, location='json' ,help='stops required')
        self.parser_put = reqparse.RequestParser()
        self.parser_put.add_argument('lat', type=float, required=True, help='latitude required!')
        self.parser_put.add_argument('lng', type=float, required=True, help='longitude required!')
        self.parser_put.add_argument('name', type=str, required=True, help='name required!')
        

    def get_route_or_abort(self, route_id):
        if route_id is None:
            abort(404, message='No route id')
            return
        
        route = RouteM.query.get(route_id)
        if route is None:
            abort(404, message=f'route for id:{route_id} doesn\'t exist')
        
        return route

    def get_or_abort(self, stop_id):
        if stop_id is None:
            abort(404, message='No stop id')
            return
        
        stop = RouteStopM.query.get(stop_id)
        if stop is None:
            abort(404, message=f'stops for id:{stop_id} doesn\'t exist')
        
        return stop

    
    @marshal_with(RouteStopM.fields)
    def get(self, route_id=None, stop_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'GET stops for {route}')
        if stop_id is None:
            return route.stops
        return self.get_or_abort(stop_id)
    
    @marshal_with(RouteStopM.fields)
    def post(self, route_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'CREATE Stops for {route}')
        args = self.parser.parse_args()
        stops_list = args['stops']
        LOGGER.debug(f'stops: {stops_list}')
        stops = []
        if args['stops']: 
            stops = [RouteStopM(**p) for p in args['stops']]
        
        LOGGER.debug(f'New stops: {stops}')
        route.stops = stops
        db.session.commit()
        return stops, 201

    @marshal_with(RouteStopM.fields)
    def put(self, route_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'ADD Stops to {route}')
        args = self.parser_put.parse_args()
        stop = RouteStopM(**args)
        LOGGER.debug(f'stop: {stop}')
        
        route.stops.append(stop)
        db.session.commit()
        return stop, 201

    @marshal_with(RouteStopM.fields)
    def patch(self, route_id=None, stop_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'UPDATE stop of {route}')
        args = self.parser_put.parse_args()
        stop = self.get_or_abort(stop_id)

        LOGGER.debug(f'stop: {stop}')
        stop.lat = args.get('lat', stop.lat)
        stop.lng = args.get('lng', stop.lng)
        stop.name = args.get('name', stop.name)
        
        db.session.commit()
        return stop, 200

    def delete(self, route_id, stop_id):
        LOGGER.info('DELETE stop')
        route = self.get_route_or_abort(route_id)
        stop = self.get_or_abort(stop_id)

        db.session.delete(stop)
        db.session.commit()

        return '', 204



class RouteCheckpoints(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('checkpoints', type=list, required=True, location='json' ,help='checkpoints required')
        self.parser_put = reqparse.RequestParser()
        self.parser_put.add_argument('lat', type=float, required=True, help='latitude required!')
        self.parser_put.add_argument('lng', type=float, required=True, help='longitude required!')
        

    def get_route_or_abort(self, route_id):
        if route_id is None:
            abort(404, message='No route id')
            return
        
        route = RouteM.query.get(route_id)
        if route is None:
            abort(404, message=f'route for id:{route_id} doesn\'t exist')
        
        return route

    def get_or_abort(self, checkpoint_id):
        if checkpoint_id is None:
            abort(404, message='No stop id')
            return
        
        checkpoint = RouteCheckpointM.query.get(checkpoint_id)
        if checkpoint is None:
            abort(404, message=f'checkpoints for id:{checkpoint_id} doesn\'t exist')
        
        return checkpoint

    
    @marshal_with(RouteCheckpointM.fields)
    def get(self, route_id=None, checkpoint_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'GET checkpoints for {route}')
        if checkpoint_id is None:
            return route.checkpoints
        return self.get_or_abort(checkpoint_id)
    
    @marshal_with(RouteCheckpointM.fields)
    def post(self, route_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'CREATE checkpoints for {route}')
        args = self.parser.parse_args()
        checkpoints_list = args['checkpoints']
        LOGGER.debug(f'checkpoints: {checkpoints_list}')
        checkpoints = []
        if args['checkpoints']: 
            checkpoints = [RouteCheckpointM(**p) for p in args['checkpoints']]
        
        LOGGER.debug(f'New checkpoints: {checkpoints}')
        route.checkpoints = checkpoints
        db.session.commit()
        return checkpoints, 201

    @marshal_with(RouteCheckpointM.fields)
    def put(self, route_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'ADD checkpoints to {route}')
        args = self.parser_put.parse_args()
        checkpoint = RouteCheckpointM(**args)
        LOGGER.debug(f'checkpoint: {checkpoint}')
        
        route.checkpoints.append(checkpoint)
        db.session.commit()
        return checkpoint, 201

    @marshal_with(RouteCheckpointM.fields)
    def patch(self, route_id=None, checkpoint_id=None):
        route = self.get_route_or_abort(route_id)
        LOGGER.info(f'UPDATE checkpoint of {route}')
        args = self.parser_put.parse_args()
        checkpoint = self.get_or_abort(checkpoint_id)

        LOGGER.debug(f'checkpoint: {checkpoint}')
        checkpoint.lat = args.get('lat', checkpoint.lat)
        checkpoint.lng = args.get('lng', checkpoint.lng)
        
        db.session.commit()
        return checkpoint, 200

    def delete(self, route_id, checkpoint_id):
        LOGGER.info('DELETE checkpoint')
        route = self.get_route_or_abort(route_id)
        checkpoint = self.get_or_abort(checkpoint_id)

        db.session.delete(checkpoint)
        db.session.commit()

        return '', 204
