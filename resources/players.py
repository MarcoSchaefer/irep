from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.player import Player, Positions
from models.republic import Republic
from guard import Auth, GetUserID, CheckPermission
import requests


bp_players = Blueprint('bp_players', __name__)

@bp_players.route('/', methods = ['GET'])
@Auth
def GetAllPlayers():
    player = Player.query.all()
    return jsonify([p.toJSON() for p in player]), 200

@bp_players.route('/<int:player_id>', methods = ['GET'])
@Auth
def GetPlayer(player_id):
    player = Player.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    return jsonify(player.toJSON()), 200

@bp_players.route('/', methods = ['POST'])
@Auth
@CheckPermission
def CreatePlayer():
    rep_exists = Republic.query.filter_by(id=request.form['republic_id']).first()
    if not rep_exists:
        return jsonify({'error':'republic not found'}), 404
    benched = request.form['benched']
    if benched in ["false","0","False"]:
        benched = False
    else:
        benched = True
    agregado = request.form['agregado']
    if agregado in ["false","0","False"]:
        agregado = False
    else:
        agregado = True
    player = Player(
        name = request.form['name'],
        republic_id = request.form['republic_id'],
        position = request.form['position'],
        value = request.form['value'],
        benched = benched,
        agregado = agregado
    )
    db.session.add(player)
    db.session.commit()
    return jsonify(player.toJSON()), 201

@bp_players.route('/<int:player_id>', methods = ['DELETE'])
@Auth
@CheckPermission
def DeletePlayer(player_id):
    player = Player.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    db.session.delete(player)
    db.session.commit()
    return jsonify({'status':'deleted'}), 201

@bp_players.route('/<int:player_id>', methods = ['PUT'])
@Auth
@CheckPermission
def ModifyPlayer(player_id):
    player = Player.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    rep_exists = Republic.query.filter_by(id=request.form['republic_id']).first()
    if not rep_exists:
        return jsonify({'error':'republic not found'}), 404
    benched = request.form['benched']
    if benched in ["false","0","False"]:
        benched = False
    else:
        benched = True
    agregado = request.form['agregado']
    if agregado in ["false","0","False"]:
        agregado = False
    else:
        agregado = True
    db.session.delete(player)
    player = Player(
        id = player_id,
        name = request.form['name'],
        republic_id = request.form['republic_id'],
        position = request.form['position'],
        value = request.form['value'],
        benched = benched,
        agregado = agregado
    )
    db.session.add(player)
    db.session.commit()
    return jsonify(player.toJSON()), 201
