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

from models.playercall import Playercall
from resources.users import bp_users
from resources.market import bp_market
from resources.players import bp_players
from resources.republics import bp_republics
from resources.teams import bp_teams
from resources.session import bp_session

app.register_blueprint(bp_session, url_prefix='/session')
app.register_blueprint(bp_users, url_prefix='/users')
app.register_blueprint(bp_players, url_prefix='/players')
app.register_blueprint(bp_republics, url_prefix='/republics')
app.register_blueprint(bp_market, url_prefix='/market')
app.register_blueprint(bp_teams, url_prefix='/teams')


@app.route('/', methods=['GET'])
def Ping():
    return "pong!", 200
