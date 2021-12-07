from flask import Flask
from flask_cors import CORS, cross_origin
from router import Router

app  = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
Router.run(app)