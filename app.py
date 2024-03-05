from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"


@app.route("/")
def show_homepage():
    game_board = boggle_game.make_board()
    session["game_board"] = game_board
    times_played = session.get("times_played", 0)
    highscore = session.get("highscore", 0)

    return render_template(
        "index.html",
        game_board=game_board,
        times_played=times_played,
        highscore=highscore,
    )


@app.route("/check")
def check_validity():
    word = request.args["guess"]
    game_board = session["game_board"]
    res = boggle_game.check_valid_word(game_board, word)

    return jsonify({"result": res})


@app.route("/game-stats", methods=["POST"])
def new_stats():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    times_played = session.get("times_played", 0)

    session["times_played"] = times_played + 1
    session["highscore"] = max(score, highscore)

    brokeRecord = score > highscore

    return jsonify({"brokeRecord": brokeRecord})
