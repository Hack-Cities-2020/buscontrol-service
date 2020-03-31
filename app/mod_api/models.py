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
        'lat': fields.Float,
        'lng': fields.Float
    }
    

    def __repr__(self):
        return f'<Route Point ({self.lat}, {self.lng})>'

# punto georeferenciado
class RouteStopM(Point):
    'Bus stop'
    __tablename__ = 'api_route_stop'
    name = db.Column(db.String(128), nullable=False, default='default stop')
    route_id = db.Column(db.Integer, db.ForeignKey('api_route.id'))

    fields = {
        'id': fields.Integer,
        'lat': fields.Float,
        'lng': fields.Float,
        'name': fields.String
    }

    def __repr__(self):
        return f'<Route Stop {self.name}:({self.lat}, {self.lng})>'

class RouteCheckpointM(Point):
    'Bus stop'
    __tablename__ = 'api_route_checkpoint'
    route_id = db.Column(db.Integer, db.ForeignKey('api_route.id'))

    fields = {
        'id': fields.Integer,
        'lat': fields.Float,
        'lng': fields.Float
    }

    def __repr__(self):
        return f'<Route Checkpoint {self.id}:({self.lat}, {self.lng})>'

# vehiculos y conductores
class DriverPerformanceM(Base):
    'Bus driver performance metrics model'
    __tablename__ = 'api_driver_performance'
    rating = db.Column(db.Integer)
    timing = db.Column(db.Integer)
    experience = db.Column(db.Integer)

    driver_id = db.Column(db.Integer, db.ForeignKey('api_driver.id'))

    def __repr__(self):
        return f'<Driver performance {self.driver_id}>'

class DriverM(Base):
    'Bus driver model'
    __tablename__ = 'api_driver'

    full_name = db.Column(db.String(128), nullable=False)
    ci = db.Column(db.String(11), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('api_vehicle.id'))
    driver_performance = db.relationship('DriverPerformanceM', backref='driver', lazy=True, uselist=False)

    fields = {
        'id': fields.String,
        'full_name': fields.String,
        'ci': fields.String
    }

    def __repr__(self):
        return f'<Driver {self.ci}>'

class VehicleM(Base):
    'Bus or vehicle model'
    __tablename__ = 'api_vehicle'

    plate = db.Column(db.String(30), nullable=False, unique=True)
    model = db.Column(db.String(90), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(90), nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    driver = db.relationship('DriverM', backref='vehicle', lazy=True, uselist=False)
    route_id = db.Column(db.Integer, db.ForeignKey('api_route.id'))

    fields = {
        'id': fields.Integer,
        'plate': fields.String,
        'model': fields.String,
        'manufacturer': fields.String,
        'year': fields.Integer,
        'capacity': fields.Integer,
        'driver': fields.Nested(DriverM.fields),
        'route_id': fields.Integer
    }

    def __init__(self, plate):
        self.plate = plate

    def __repr__(self):
        return f'<Vehicle {self.plate}>'


# Rutas
class RouteM(Base):
    'Route model'
    __tablename__ = 'api_route'

    name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    path_color = db.Column(db.String(30), nullable=False)
    path = db.Column(db.Text, nullable=True)
    stops = db.relationship('RouteStopM', backref='route', lazy=True)
    checkpoints = db.relationship('RouteCheckpointM', backref='route', lazy=True)
    vehicles = db.relationship('VehicleM', backref='route', lazy=True)

    fields = {
        'id': fields.Integer,
        'name': fields.String,
        'status': fields.String,
        'path_color': fields.String,
        'path': PointFields,
        'stops': fields.List(fields.Nested(RouteStopM.fields)),
        'checkpoints': fields.List(fields.Nested(RouteCheckpointM.fields)),
        'vehicles': fields.List(fields.Nested(VehicleM.fields))
    }

    def __init__(self, name, status, path_color='', path='', stops=None, checkpoints=None):
        self.name = name
        self.status = status
        self.path_color = path_color
        self.path = path
        self.stops = stops if stops else []
        self.checkpoints = checkpoints if checkpoints else []
    
    def __repr__(self):
        return f'<Route {self.name}>'

