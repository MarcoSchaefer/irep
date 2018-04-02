from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.player import Player
from guard import Auth, GetUserID
import requests


bp_player = Blueprint('bp_player', __name__)

@bp_player.route('/', methods = ['GET'])
@Auth
def Ping():
    return "pong",200;
