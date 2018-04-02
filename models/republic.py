from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.player import Player
from models.team import Team

class Republic(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    address = db.Column(db.Text, unique=False, nullable=False)
    players = db.relationship("Player")
    picture = db.Column(db.Text, unique=False, nullable=True)


    def __repr__(self):
        return '<id:%r>' % (self.id)

    def toJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'value':self.value,
            'picture': self.picture
            }
