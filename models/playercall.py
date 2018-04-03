from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db

class Playercall(db.Model):
    player_id = db.Column(mysql.INTEGER(50), db.ForeignKey('player.id'), primary_key=True)
    team_id = db.Column(mysql.INTEGER(50), db.ForeignKey('team.id'), primary_key=True)

    def toJSON(self):
        return {
            'player_id': self.player_id,
            'team_id': self.team_id
            }
