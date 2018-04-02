from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.republic import Republic
from models.team import Team

class Player(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    republic_id = db.Column(db.Integer, db.ForeignKey('republic.id'))
    republic = db.relationship("Republic")
    teams = db.relationship("Team")
    picture = db.Column(db.Text, unique=False, nullable=True)
    position = db.Column(db.String(120), unique=False, nullable=False)
    value = db.Column(mysql.INTEGER(50), unique=False, nullable=False)


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
