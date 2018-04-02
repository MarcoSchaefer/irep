from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.role import Role
#from models.team import Team

class User(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship("Role")
    regDate = db.Column(mysql.INTEGER(50), unique=False, nullable=False)
    team = db.relationship("Team")
    picture = db.Column(db.Text, unique=False, nullable=True)
    coins = db.Column(mysql.INTEGER(50), primary_key=True)


    def __repr__(self):
        return '<User id:%r email:%r role:%r>' % (self.id, self.email, self.role)

    def toJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.toJSON(),
            'regDate': self.regDate,
            'team':self.team.toJSONmin(),
            'picture': self.picture
            }

    def toJSONmin(self):
        return {
            'id': self.id,
            'name': self.name,
            'regDate': self.regDate,
            'picture': self.picture
            }
