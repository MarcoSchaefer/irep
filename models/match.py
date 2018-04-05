from sqlalchemy.dialects import mysql
import enum
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db

class Match(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    republic_home_id = db.Column(db.Integer, db.ForeignKey('republic.id'),nullable=False)
    republic_away_id = db.Column(db.Integer, db.ForeignKey('republic.id'),nullable=False)
    republic = db.relationship("Republic")
    score_home = db.Column(mysql.INTEGER(50), unique=False, nullable=True)
    score_away = db.Column(mysql.INTEGER(50), unique=False, nullable=True)
    time = db.Column(db.String(100), unique=False, nullable=True)
    place = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<id:%r>' % (self.id)

    def toJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'republic':self.republic.toJSONmin(),
            'position': self.position.name,
            'value':self.value,
            'benched': self.benched,
            'agregado': self.agregado
            }

    def toJSONmin(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position.name,
            'value':self.value
            }
