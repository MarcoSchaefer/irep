from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.market import Market
from guard import Auth, GetUserID
import requests


bp_market = Blueprint('bp_market', __name__)

@bp_market.route('/', methods = ['GET'])
@Auth
def Ping():
    return "pong",200;
