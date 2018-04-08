from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.playercall import playercall_table

class Team(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="teams")
    players = db.relationship("Player",secondary=playercall_table)
    #points = db.relationship("TeamPoints")


    def __repr__(self):
        return '<id:%r>' % (self.id)

    def toJSON(self):
        players = [p.toJSON() for p in self.players]
        return {
            'id': self.id,
            'name': self.name,
            #'points':self.points,
            'user': self.user.toJSONmin(),
            'players':[p.toJSON() for p in self.players]
            }
