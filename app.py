from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Puzzle Backend Live!"

if __name__ == "__main__":
    app.run()
from flask import Flask, request, jsonify
from database import db
from models import Player, Game
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///puzzle.db"
db.init_app(app)

with app.app_context():
    db.create_all()

# Home
@app.route("/")
def home():
    return "Puzzle Game Backend Running"

# Create player
@app.route("/player", methods=["POST"])
def create_player():
    data = request.get_json()
    player = Player(username=data["username"])
    db.session.add(player)
    db.session.commit()
    return jsonify({"player_id": player.id})

# Start new game
@app.route("/game", methods=["POST"])
def new_game():
    data = request.get_json()
    player_id = data["player_id"]
    secret_number = random.randint(1, 10)
    game = Game(player_id=player_id, secret_number=secret_number)
    db.session.add(game)
    db.session.commit()
    return jsonify({"game_id": game.id})

# Make a guess
@app.route("/guess/<int:game_id>", methods=["POST"])
def guess(game_id):
    data = request.get_json()
    user_guess = data["guess"]
    game = Game.query.get(game_id)
    if game.completed:
        return jsonify({"message": "Game already completed"})

    game.attempts += 1

    if user_guess == game.secret_number:
        game.completed = True
        db.session.commit()
        return jsonify({"result": "Correct!", "attempts": game.attempts})
    elif user_guess < game.secret_number:
        db.session.commit()
        return jsonify({"result": "Too low"})
    else:
        db.session.commit()
        return jsonify({"result": "Too high"})
