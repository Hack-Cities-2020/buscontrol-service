# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
# Import the database object from the main app module
from app import db
# Import module models (i.e. User)
from app.mod_test.models import AnimalM
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_test = Blueprint('test', __name__, url_prefix='/test')

# Set the route and accepted methods
@mod_test.route('/animal/', methods=['GET'])
def get_animal():
    # If sign in form is submitted
    animals = AnimalM.query.all()
    
    return animals[0].name