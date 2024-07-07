from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)