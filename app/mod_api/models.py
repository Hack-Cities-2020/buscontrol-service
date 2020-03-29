import json
from flask_restful import fields
from app import db
from app.models import Base, Point


json_path_fields = {
   'lat': fields.Float,
   'lng': fields.Float 
}

class PointFields(fields.Raw):
    def format(self, value):
        if value == 'null' or value is None or value == '':
            return []
        return json.loads(value)
# punto georeferenciado
class RoutePointM(Point):
    'Point for the route path'
    __tablename__ = 'api_route_point'
    route_id = db.Column(db.Integer, db.ForeignKey('api_route.id'))

    fields = {
        'lat': fields.Float(attribute='latitude'),
        'lng': fields.Float(attribute='longitude')
    }
    
    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long

    def __repr__(self):
        return f'<Route Point ({self.latitude}, {self.longitude})>'

# punto georeferenciado
class RouteStopM(Point):
    'Bus stop'
    __tablename__ = 'api_route_stop'
    name = db.Column(db.String(128), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('api_route.id'))

    fields = {
        'id': fields.Integer,
        'lat': fields.Float(attribute='latitude'),
        'lng': fields.Float(attribute='longitude'),
        'name': fields.String
    }

    def __init__(self, lat, long, name='default stop'):
        self.latitude = lat
        self.longitude = long
        self.name = name

    def __repr__(self):
        return f'<Route Stop {self.name}:({self.latitude}, {self.longitude})>'

class RouteCheckpointM(Point):
    'Bus stop'
    __tablename__ = 'api_route_checkpoint'
    route_id = db.Column(db.Integer, db.ForeignKey('api_route.id'))

    fields = {
        'id': fields.Integer,
        'lat': fields.Float(attribute='latitude'),
        'lng': fields.Float(attribute='longitude')
    }
    
    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long

    def __repr__(self):
        return f'<Route Checkpoint {self.id}:({self.latitude}, {self.longitude})>'
# Rutas
class RouteM(Base):
    'Route model'
    __tablename__ = 'api_route'

    name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    path = db.relationship('RoutePointM', backref='route', lazy=True)
    stops = db.relationship('RouteStopM', backref='route', lazy=True)
    checkpoints = db.relationship('RouteCheckpointM', backref='route', lazy=True)
    json_path = db.Column(db.Text, nullable=True)

    fields = {
        'id': fields.Integer,
        'name': fields.String,
        'status': fields.String,
        'path': fields.List(fields.Nested(RoutePointM.fields)),
        'stops': fields.List(fields.Nested(RouteStopM.fields)),
        'checkpoints': fields.List(fields.Nested(RouteCheckpointM.fields)),
        'json_path': PointFields
    }

    def __init__(self, name, status, path=None, stops=None, checkpoints=None, json_path=''):
        self.name = name
        self.status = status
        self.path = path if path else []
        self.stops = stops if stops else []
        self.checkpoints = checkpoints if checkpoints else []
        self.json_path = json_path
    
    def __repr__(self):
        return f'<Route {self.name}>'


# vehiculos y conductores

class Vehicle(Base):
    'Bus or vehicle model'
    __tablename__ = 'api_vehicle'

    plate = db.Column(db.String(30), nullable=False, unique=True)
    model = db.Column(db.String(90), nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Driver(Base):
    'Bus driver model'
    __tablename__ = 'api_driver'

    name = db.Column(db.String(128), nullable=False)
    las_name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    ci = db.Column(db.String(11), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30), nullable=False)
