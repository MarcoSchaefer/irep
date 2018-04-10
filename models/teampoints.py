from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db


class TeamPoints(db.Model):
    team_id = db.Column(mysql.INTEGER(50), db.ForeignKey('team.id'), primary_key=True)
    round = db.Column(mysql.INTEGER(50), primary_key=True)


    def __repr__(self):
        return 'team_id:%r round:%r' % (self.team_id,self.round)

    def toJSON(self):
        return {
            'team_id': self.team_id,
            'round': self.round
            }
