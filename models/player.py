from sqlalchemy.dialects import mysql
from functools import reduce
from sqlalchemy.types import Enum
import enum
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.playercall import playercall_table
from models.playerpoints import PlayerPoints

class Positions(enum.Enum):
    Goleiro = 1
    Linha = 2

class Player(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    republic_id = db.Column(db.Integer, db.ForeignKey('republic.id'),nullable=False)
    republic = db.relationship("Republic", lazy="joined")
    teams = db.relationship("Team",secondary=playercall_table)
    position = db.Column(Enum(Positions), unique=False, nullable=False)
    value = db.Column(db.Float, unique=False, nullable=False)
    benched = db.Column(db.Boolean, unique=False, nullable=False)
    points = db.relationship(PlayerPoints, cascade="delete", lazy="joined")

    def __repr__(self):
        return '<id:%r position:%r>' % (self.id, self.position)

    def toJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'republic':self.republic.toJSONmin(),
            'position': self.position.name,
            'value':float("{0:.2f}".format(self.value)),
            'benched': self.benched,
            'average': float("{0:.2f}".format(self.getAveragePoints())),
            'last': float("{0:.2f}".format(self.getLastPoints())),
            'points': [p.toJSONmin() for p in self.points]
            }

    def toJSONmin(self):
        return {
            'id': self.id,
            'name': self.name,
            'republic':self.republic.toJSONmin(),
            'position': self.position.name,
            'value':float("{0:.2f}".format(self.value)),
            'benched': self.benched,
            'average': float("{0:.2f}".format(self.getAveragePoints())),
            'last': float("{0:.2f}".format(self.getLastPoints()))
            }

    def getLastPoints(self):
        if not self.points:
            return 0
        return self.points[-1].points

    def getPointsInRound(self,round):
        points = PlayerPoints.query.filter_by(player_id=self.id,round=round).first()
        if not points:
            return 0
        return points.points

    def getAveragePoints(self):
        pointsCopy = [p.points for p in self.points]
        pointsCopy.append(5)
        return reduce((lambda x, y: x + y), [p for p in pointsCopy])/len(pointsCopy)

    def newScore(self,score,round):
        m = self.getAveragePoints()
        points = PlayerPoints.query.filter_by(player_id=self.id,round=round).first()
        if not points:
            newPoints = PlayerPoints(
                player_id = self.id,
                round = round,
                points = score
                )
            db.session.add(newPoints)
            self.points.append(newPoints)
        else:
            points.points = score
            db.session.merge(points)
        self.value = self.getNextValue(m)
        return self

    def getNextValue(self,previous_m):
        t = 20
        k = 0.15
        if self.value >= 10:
            k = 0.5
        if self.value >= 6 and self.value < 10:
            k=0.25
        c = self.value
        p = self.getLastPoints()
        m = previous_m
        x = (p-m)*k
        print(m)
        a = (t-c)/t
        v = x*a
        return self.value + v
