from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.team import Team
from models.player import Player
from guard import Auth, GetUserID, getUserFromRequest
import requests


bp_teams = Blueprint('bp_teams', __name__)

@bp_teams.route('/', methods = ['GET'])
@Auth
def GetAllTeams():
    teams = Team.query.all()
    return jsonify([t.toJSON() for t in teams]),200;

@bp_teams.route('/me', methods = ['GET'])
@Auth
def GetOwnTeams():
    user = getUserFromRequest()
    if len(user.teams) == 0:
        return jsonify({"error":"you don't have a team"}), 400
    return jsonify(user.teams[0].toJSON()),200;

@bp_teams.route('/me/players', methods = ['POST'])
@Auth
def AddPlayerToTeam():
    user = getUserFromRequest()
    if len(user.teams) == 0:
        return jsonify({"error":"you don't have a team"}), 400
    player = Player.query.filter_by(id = request.form['player_id']).first()
    if not player:
        return jsonify({"error":"player not found"}), 400
    if user.coins < player.value:
        return jsonify({"error":"insufficient coins"}), 401
    print(player.position)
    if player in user.teams[0].players:
        return jsonify({"error":"you already have this player in your team"}), 400
    user.teams[0].players.append(player)
    user.coins = user.coins - player.value
    db.session.commit()
    return jsonify(user.teams[0].toJSON()),200;

@bp_teams.route('/', methods = ['POST'])
@Auth
def CreateTeam():
    user = getUserFromRequest()
    if len(user.teams) > 0:
        return jsonify({"error":"you already have a team"}), 401
    team = Team(
        name = request.form['name'],
        user_id = GetUserID(),
        points = 0
        )
    db.session.add(team)
    db.session.commit()
    return jsonify(team.toJSON()),201;
