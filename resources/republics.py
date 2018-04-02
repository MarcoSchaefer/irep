from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.republic import Republic
from guard import Auth, GetUserID
import requests


bp_republics = Blueprint('bp_republics', __name__)

@bp_republics.route('/', methods = ['GET'])
@Auth
def Ping():
    return "pong",200;
