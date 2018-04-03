from flask import Blueprint, jsonify, request
import requests
import time
import jwt

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from config import JWT_LIFETIME
from models.user import User
from utils import DecodeToken, encrypt, CreateToken


bp_session = Blueprint('bp_session', __name__)

@bp_session.route('/login', methods = ['POST'])
def Login():
    email = request.form['email']
    password = request.form['password']
    if len(password):
        password = encrypt(password)
    user = User.query.filter_by(email=request.form['email']).first()
    if not user:
        return jsonify({'error':'email not registered'}), 401
    if not user.password:
        return jsonify({'error':'this account can only be accessed through facebook authentication'}), 400
    if not user.password == password:
        return jsonify({'error':'wrong password'}), 401
    token = CreateToken({'user_id':user.id,'exp':int(time.time())+JWT_LIFETIME})
    return jsonify({'status':'success','token':token}), 200

#Necessita do token de acesso do FB enviado no header Authentication
@bp_session.route('/FBlogin', methods=['POST'])
def FBLogin():
    FBtoken = request.headers.get('authorization')
    print(FBtoken)
    fbresponse = requests.post("https://graph.facebook.com/me?fields=name,picture,email", headers={"Authorization":FBtoken})
    if fbresponse.status_code >= 400:
        print(fbresponse)
        return jsonify({'error':'invalid token'}), 401
    fbresponse = fbresponse.json()
    if not fbresponse['email']:
        return jsonify({'error':"facebook api didn't returned any email"}), 500
    user = User.query.filter_by(email=fbresponse['email']).first()
    if user:
        return jsonify(user.toJSON()), 200
    user = User(
        email = fbresponse['email'],
        name = fbresponse['name'],
        role_id = 1,
        regDate = time.time(),
        coins = 0,
        picture = fbresponse['picture']['data']['url']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.toJSON()), 201


@bp_session.route('/refresh', methods=['GET'])
def refreshToken():
    if not request.headers.get('authorization'):
        return jsonify({'error':'a token is required'}), 401
    auth = request.headers.get('authorization')
    try:
        token = DecodeToken(auth)
    except jwt.ExpiredSignatureError:
        return jsonify({'error':'token timeout'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error':'invalid token'}), 401
    oldToken = DecodeToken(request.headers.get('authorization'))
    token = CreateToken({'user_id':oldToken['user_id'],'exp':int(time.time())+JWT_LIFETIME})
    return jsonify({'status':'success','token':token}), 200
