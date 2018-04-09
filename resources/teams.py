from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.team import Team
from models.player import Player
from models.market import Market
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
        return jsonify({"error":"insufficient coins"}), 400
    has_gk = False
    for p in user.teams[0].players:
        if p.position.name=="Goleiro":
            has_gk = True
    if player in user.teams[0].players:
        return jsonify({"error":"you already have this player in your team"}), 400
    if has_gk and player.position.name == "Goleiro":
        return jsonify({"error":"you already have a goalkeeper"}), 400
    if player.benched:
        return jsonify({"error":"this player is benched"}), 400
    user.teams[0].players.append(player)
    user.coins = user.coins - player.value
    db.session.commit()
    return jsonify(user.teams[0].toJSON()),200;

@bp_teams.route('/me/players/<int:player_id>', methods = ['DELETE'])
@Auth
def SellPlayer(player_id):
    player = Player.query.filter_by(id = player_id).first()
    if not player:
        return jsonify({"error":"player not found"}), 400
    user = getUserFromRequest()
    if len(user.teams) == 0:
        return jsonify({"error":"you don't have a team"}), 400
    market = Market.query.first()
    if not market.open:
        return jsonify({"error":"the market is closed"}), 400
    if player not in user.teams[0].players:
        return jsonify({"error":"this player isn't in your team"}), 400
    user.coins = user.coins + player.value
    user.teams[0].players.remove(player)
    db.session.commit()
    return jsonify({"status":"sold"}),201

@bp_teams.route('/', methods = ['POST'])
@Auth
def CreateTeam():
    user = getUserFromRequest()
    if len(user.teams) > 0:
        return jsonify({"error":"you already have a team"}), 400
    team = Team(
        name = request.form['name'],
        user_id = GetUserID()
        )
    db.session.add(team)
    db.session.commit()
    return jsonify(team.toJSON()),201;

@bp_teams.route('/me/name', methods = ['PUT'])
@Auth
def ChangeTeamName():
    team = Team.query.filter_by(user_id = GetUserID()).first()
    if not team:
        return jsonify({"error":"Time não encontrado"}), 400
    team.name = request.form['name']
    db.session.merge(team)
    db.session.commit()
    return jsonify(team.toJSON()),201

@bp_teams.route('/me', methods = ['PUT'])
@Auth
def ChangeTeamPlayers():
    team = Team.query.filter_by(user_id = GetUserID()).first()
    if not team:
        return jsonify({"error":"Time não encontrado"}), 400
    playersids = request.form.getlist('players')
    if not playersids or len(playersids)<5:
        return jsonify({"error":"Seu time precisa ter 5 jogadores"}), 400
    players = [Player.query.filter_by(id=p).first() for p in playersids]
    db.session.merge(team)
    db.session.commit()
    return jsonify(team.toJSON()),201
