from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Puzzle Backend Live!"

if __name__ == "__main__":
    app.run()
