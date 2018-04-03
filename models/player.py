from sqlalchemy.dialects import mysql
from sqlalchemy.types import Enum
import enum
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db

class Positions(enum.Enum):
    Goleiro = 1
    Linha = 2

class Player(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    republic_id = db.Column(db.Integer, db.ForeignKey('republic.id'),nullable=False)
    republic = db.relationship("Republic")
    position = db.Column(Enum(Positions), unique=False, nullable=False)
    value = db.Column(mysql.INTEGER(50), unique=False, nullable=False)
    benched = db.Column(db.Boolean, unique=False, nullable=False)
    agregado = db.Column(db.Boolean, unique=False, nullable=False)

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
