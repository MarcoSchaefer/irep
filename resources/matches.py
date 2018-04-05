from flask import Blueprint, jsonify, request
from sqlalchemy import or_

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.match import Match
from guard import Auth, GetUserID, CheckPermission
import requests


bp_matches = Blueprint('bp_matches', __name__)

@bp_matches.route('/', methods = ['GET'])
@Auth
def GetAllMatches():
    matches = Match.query.all()
    return jsonify([m.toJSON() for m in matches]),200;

@bp_matches.route('/current', methods = ['GET'])
@Auth
def GetCurrentMatches():
    matches = Match.query.filter(or_(Match.score_home==None,Match.score_away==None)).all()
    return jsonify([m.toJSON() for m in matches]),200;

@bp_matches.route('/', methods = ['POST'])
@Auth
@CheckPermission
def CreateMatch():
    if request.form['republic_home_id'] == request.form['republic_away_id']:
        return jsonify({'error':'Dois times iguais foram selecionados'}),400;
    match = Match(
        republic_home_id = request.form['republic_home_id'],
        republic_away_id = request.form['republic_away_id'],
        time = request.form['time'],
        place = request.form['place'],
        )
    db.session.add(match)
    db.session.commit()
    return jsonify(match.toJSON()),201;

@bp_matches.route('/<int:match_id>', methods = ['PUT'])
@Auth
@CheckPermission
def UpdateMatch(match_id):
    match = Match.query.filter_by(id=match_id).first()
    if not match:
        return jsonify({'error':'Partida não encontrada'}),400;
    match.score_home = request.form['score_home']
    match.score_away = request.form['score_away']
    db.session.merge(match)
    db.session.commit()
    return jsonify(match.toJSON()),201;

@bp_matches.route('/<int:match_id>', methods = ['DELETE'])
@Auth
@CheckPermission
def DeleteMatch(match_id):
    match = Match.query.filter_by(id=match_id).first()
    if not match:
        return jsonify({'error':'Partida não encontrada'}),400;
    db.session.delete(match)
    db.session.commit()
    return jsonify({'status':'Partida apagada com sucesso'}),201;
