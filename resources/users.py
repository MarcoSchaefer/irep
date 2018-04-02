from flask import Blueprint, jsonify, request, send_file
import time
from werkzeug.utils import secure_filename

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.user import User
from utils import encrypt, isValidEmail, allowed_file
from config import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from guard import Auth, GetUserID
import requests


bp_users = Blueprint('bp_users', __name__)

@bp_users.route('/<int:user_id>/picture', methods = ['GET'])
@Auth
def GetPicture(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':'user not found'}), 400
    if not user.picture:
        return jsonify({'error':'user picture not found'}), 400
    if len(user.picture.split('.')) > 3:
        return jsonify({'picture_url':user.picture}), 200
    return send_file(user.picture, mimetype='image/gif')


@bp_users.route('/me/picture', methods = ['POST'])
@Auth
def ChangePicture():
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'error':'no image received'}), 400
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        return jsonify({'error':'invalid file'}), 400
    user_id = GetUserID()
    filename = secure_filename(file.filename)
    filename = str(user_id)+'.'+filename.split('.')[1]
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    user = User.query.filter_by(id=user_id).first()
    user.picture = UPLOAD_FOLDER+"/"+filename
    db.session.commit()
    return jsonify({'status':'success'}), 200

@bp_users.route('/', methods = ['POST'])
def Register():
    if not isValidEmail(request.form['email']):
        return jsonify({'error':'invalid email'}), 400
    if len(request.form['password'])<PASSWORD_MIN_LENGTH:
        return jsonify({'error':'password too short'}), 400
    if len(request.form['password'])>PASSWORD_MAX_LENGTH:
        return jsonify({'error':'password too long'}), 400
    exists = User.query.filter_by(email=request.form['email']).first()
    if exists:
        return jsonify({'error':'email already registered'}), 400
    name = request.form['name']
    if not len(name):
        name = None
    user = User(
        email = request.form['email'],
        password = encrypt(request.form['password']),
        name = name,
        role_id = 1,
        regDate = time.time(),
        coins = 0
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.toJSON()), 201


@bp_users.route('/', methods = ['GET'])
@Auth
def GetAllUsers():
    users = User.query.all()
    users = [u.toJSONmin() for u in users]
    return jsonify(users), 200

@bp_users.route('/me', methods = ['GET'])
@Auth
def GetOwnInfo():
    user_id = GetUserID()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':"user not found"}), 500
    return jsonify(user.toJSON()), 200

@bp_users.route('/<int:user_id>', methods = ['GET'])
@Auth
def GetUserInfo(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':"user not found"}), 500
    return jsonify(user.toJSONmin()), 200

@bp_users.route('/FBlogin', methods = ['POST'])
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

@bp_users.route('/me', methods = ['PUT'])
@Auth
def EditProfile():
    user_id = GetUserID()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':"user not found"}), 500
    name = request.form['name']
    birthday = request.form['birthday']
    user.name = name
    user.birthday = birthday
    db.session.commit()
    return jsonify(user.toJSON()), 200

@bp_users.route('/login', methods = ['POST'])
def Login():
    email = request.form['email']
    password = request.form['password']
    if len(password):
        password = encrypt(password)
    user = User.query.filter_by(email=request.form['email']).first()
    if not user.password:
        return jsonify({'error':'this account can only be accessed through facebook authentication'}), 400
    if not user:
        return jsonify({'error':'email not registered'}), 400
    if not user.password == password:
        return jsonify({'error':'wrong password'}), 400
    return jsonify(user.toJSON()), 200
