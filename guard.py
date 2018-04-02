from flask import request, jsonify
import time
from functools import wraps

import requests

def Auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.headers.get('authorization'):
            return jsonify({'error':'a token is required'}), 401
        auth = request.headers.get('authorization').split(" ", 2)[1]
        try:
            token = jwt.decode(auth, JWT_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error':'token timeout'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error':'invalid token'}), 401
        return jsonify(token), 200
    return decorated

def GetUserID():
    if not request.headers.get('authorization'):
        return jsonify({'error':'a token is required'}), 401
    token = auth.split(" ", 2)[1]
    token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    return token['user_id']
