from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.market import Market
from guard import Auth, GetUserID, CheckPermission
import requests


bp_market = Blueprint('bp_market', __name__)

@bp_market.route('/', methods = ['GET'])
@Auth
def GetMarket():
    market = Market.query.first()
    return jsonify(market.toJSON()),200;

@bp_market.route('/', methods = ['PUT'])
@Auth
@CheckPermission
def ToggleMarket():
    market = Market.query.first()
    market.open = not market.open
    db.session.merge(market)
    db.session.commit()
    return jsonify(market.toJSON()),200;
