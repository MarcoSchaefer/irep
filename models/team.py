from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.user import User
#from models.player import Player

class Team(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    players = db.relationship("Player")
    formation = db.Column(db.String(120), unique=False, nullable=False)
    points = db.Column(mysql.INTEGER(50), unique=False, nullable=False)
    last_points = db.Column(mysql.INTEGER(50), unique=False, nullable=True)


    def __repr__(self):
        return '<id:%r>' % (self.id)

    def toJSON(self):
        players = [p.toJSON() for p in self.players]
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'value':self.value,
            'players':players,
            'picture': self.picture
            }
