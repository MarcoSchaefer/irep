from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.player import Player, Positions
from models.republic import Republic
from models.market import Market
from models.playerpoints import PlayerPoints
from models.playercall import playercall_table
from guard import Auth, GetUserID, CheckPermission
import requests


bp_players = Blueprint('bp_players', __name__)

@bp_players.route('/', methods = ['GET'])
@Auth
def GetAllPlayers():
    player = Player.query.all()
    return jsonify([p.toJSON() for p in player]), 200

@bp_players.route('/active', methods = ['GET'])
@Auth
def GetActivePlayers():
    player = Player.query.filter_by(benched=False).all()
    players = [p.toJSON() for p in player]
    players.sort(key=lambda player: player['average'], reverse=True)
    return jsonify(players), 200

@bp_players.route('/<int:player_id>', methods = ['GET'])
@Auth
def GetPlayer(player_id):
    player = Player.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 400
    return jsonify(player.toJSON()), 200

@bp_players.route('/', methods = ['POST'])
@Auth
@CheckPermission
def CreatePlayer():
    rep_exists = Republic.query.filter_by(id=request.form['republic_id']).first()
    if not rep_exists:
        return jsonify({'error':'republic not found'}), 400
    benched = request.form['benched']
    if benched in ["false","0","False"]:
        benched = False
    else:
        benched = True
    if float(request.form['value']) <= 0:
        return jsonify({'error':'Valor inválido'}), 400
    player = Player(
        name = request.form['name'],
        republic_id = request.form['republic_id'],
        position = request.form['position'],
        value = request.form['value'],
        benched = benched
    )
    db.session.add(player)
    db.session.commit()
    if player.position=="":
        db.session.delete(player)
        db.session.commit()
        return jsonify({'error':'Posição inválida'}), 400
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

@bp_players.route('/most-points', methods = ['GET'])
@Auth
def MostPoints():
    market = Market.query.first()
    points = PlayerPoints.query.filter_by(round=market.round).order_by(PlayerPoints.points.desc()).all()
    points = [p.toJSON() for p in points]
    pointsGoleiro = list(filter(lambda x: x['player']['position'] == "Goleiro", points))
    pointsLinha = list(filter(lambda x: x['player']['position'] == "Linha", points))
    return jsonify({"Goleiro":pointsGoleiro[:1],"Linha":pointsLinha[:4]}), 200

@bp_players.route('/most-choosen', methods = ['GET'])
@Auth
def MostChoosen():
    #players = Player.query.all()
    #for p in players:
    #    p.n_teams = len(p.teams)
    #players.sort(key=lambda player: player['average'], reverse=True)
    return jsonify([]), 200

@bp_players.route('/<int:player_id>/bench', methods = ['PUT'])
@Auth
@CheckPermission
def BenchPlayer(player_id):
    player = Player.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    player.benched = not player.benched;
    db.session.merge(player)
    db.session.commit()
    return jsonify(player.toJSON()), 201

@bp_players.route('/<int:player_id>/points', methods = ['POST'])
@Auth
@CheckPermission
def GivePlayerPoints(player_id):
    player = Player.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    player.value = request.form['value']
    db.session.merge(player)
    db.session.commit()
    return jsonify(player.toJSON()),200

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
    db.session.delete(player)
    player = Player(
        id = player_id,
        name = request.form['name'],
        republic_id = request.form['republic_id'],
        position = request.form['position'],
        value = request.form['value'],
        benched = benched
    )
    db.session.add(player)
    db.session.commit()
    return jsonify(player.toJSON()), 201


@bp_players.route('/scores', methods = ['PUT'])
@Auth
@CheckPermission
def GivePlayersScore():
    market = Market.query.first()
    if market.open:
        return jsonify({'error':'Você não pode dar pontos a um jogador enquanto o mercado estiver aberto'}),400;
    playersids = request.form.getlist('players')
    for pid in playersids:
        player = Player.query.filter_by(id=pid).first()
        if not player:
            return jsonify({'error':'Um dos jogadores relacionados não foi encontrado. ID: '+pid}),400;
    players = [Player.query.filter_by(id=pid).first() for pid in playersids]
    points = request.form.getlist('points')
    if not len(points) == len(players):
        return jsonify({'error':'Número de argumentos inválido'}),400;
    for pindex in range(len(players)):
        playerpoints = PlayerPoints.query.filter_by(player_id = players[pindex].id,round=market.round).first()
        if playerpoints:
            for t in players[pindex].teams:
                t.newScore(-1*players[pindex].getPointsInRound(market.round),market.round)
        players[pindex].newScore(float(points[pindex]),market.round)
        for t in players[pindex].teams:
            t.newScore(float(points[pindex]),market.round)
    for p in players:
        db.session.merge(p)
    db.session.commit()
    return jsonify([p.toJSON() for p in players]),201;
