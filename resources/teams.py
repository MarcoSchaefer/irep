from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.team import Team
from guard import Auth, GetUserID
import requests


bp_team = Blueprint('bp_team', __name__)

@bp_team.route('/', methods = ['GET'])
@Auth
def Ping():
    return "pong",200;
