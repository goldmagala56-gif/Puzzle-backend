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
    return "Advanced Puzzle Backend Running"

# Create Player
@app.route("/player", methods=["POST"])
def create_player():
    data = request.get_json()
    player = Player(username=data["username"])
    db.session.add(player)
    db.session.commit()
    return jsonify({"player_id": player.id})

# Start Game
@app.route("/game", methods=["POST"])
def start_game():
    data = request.get_json()
    puzzle_type = data["puzzle_type"]
    player_id = data["player_id"]

    if puzzle_type == "number":
        secret = str(random.randint(1, 20))
    elif puzzle_type == "word":
        words = ["code", "python", "logic", "game"]
        secret = random.choice(words)
    else:
        return jsonify({"error": "Invalid puzzle type"})

    game = Game(player_id=player_id, puzzle_type=puzzle_type, secret_value=secret)
    db.session.add(game)
    db.session.commit()

    return jsonify({"game_id": game.id, "puzzle_type": puzzle_type})

# Guess
@app.route("/guess/<int:game_id>", methods=["POST"])
def make_guess(game_id):
    data = request.get_json()
    guess = str(data["guess"])

    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"})

    if game.completed:
        return jsonify({"message": "Game already completed"})

    game.attempts += 1

    if guess == game.secret_value:
        game.completed = True
        game.score = max(100 - (game.attempts * 10), 10)
        db.session.commit()
        return jsonify({"result": "Correct!", "score": game.score})

    db.session.commit()
    return jsonify({"result": "Wrong guess", "attempts": game.attempts})

# Leaderboard
@app.route("/leaderboard")
def leaderboard():
    top_games = Game.query.filter_by(completed=True).order_by(Game.score.desc()).limit(10).all()

    results = []
    for game in top_games:
        player = Player.query.get(game.player_id)
        results.append({
            "username": player.username,
            "score": game.score,
            "puzzle_type": game.puzzle_type
        })

    return jsonify(results)from flask import Flask
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
