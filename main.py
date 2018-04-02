from flask import Flask, jsonify, request, session
from flask_cors import CORS
from config import APPLICATION_PREFIX, JWT_LIFETIME, JWT_KEY, DATABASE_URI,MAX_CONTENT_LENGTH,UPLOAD_FOLDER
from prefix_middleware import PrefixMiddleware
from flask_sqlalchemy import SQLAlchemy
import jwt
import time

app = Flask(__name__)
CORS(app)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=APPLICATION_PREFIX)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
db = SQLAlchemy(app)

#from resources.users import bp_users

#app.register_blueprint(bp_users)

@app.route('/', methods=['GET'])
def Ping():
    return "pong!", 200
