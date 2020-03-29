from flask import Blueprint
from flask_restful import Api
from app.mod_api.resources import Animal

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod_api)

## routes
api.add_resource(Animal, '/animal', '/animal/<string:animal_id>')
