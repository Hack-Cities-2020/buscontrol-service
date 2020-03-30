from flask import Blueprint
from flask_restful import Api
from app.mod_api.resources import Route, Vehicle

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod_api)

## routes
# api.add_resource(Animal, '/animal', '/animal/<string:animal_id>')

api.add_resource(Route, '/route', '/route/<route_id>')

api.add_resource(Vehicle, '/vehicle', '/vehicle/<vehicle_id>')

