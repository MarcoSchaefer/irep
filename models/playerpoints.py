from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db


class PlayerPoints(db.Model):
    player_id = db.Column(mysql.INTEGER(50), db.ForeignKey('player.id'), primary_key=True)
    round = db.Column(mysql.INTEGER(50), primary_key=True)


    def __repr__(self):
        return 'player_id:%r round:%r' % (self.player_id,self.round)

    def toJSON(self):
        return {
            'player_id': self.player_id,
            'round': self.round
            }
