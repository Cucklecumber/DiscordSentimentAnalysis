from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import ast

app = Flask(__name__)

api = Api(app)

class Users(Resource):
    pass

api.add_resource(Users, '/users') #/user is entry point


