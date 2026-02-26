from database import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"))
    secret_number = db.Column(db.Integer)
    attempts = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
