from flask import Flask, request, redirect, render_template, flash, jsonify, session, Response
from boggle import Boggle
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"


boggle_game = Boggle()

@app.route("/")
def home_page():
    """Renders home page"""
    return render_template('home.html')


@app.route('/boggle')
def boggle():
    """Creates and starts a game of boggle"""
    game = game=boggle_game.make_board()
    session["game"] = game
    session['guesses'] = []
    return render_template('boggle.html',game=game)


@app.route('/guess', methods=["POST"])
def make_guess():
    """Accepts a guess in a POST request and checks to see if it is a valid word in the boggle game, if it is returns status 200"""
    data = request.json
    guess = data.get("guess")
    guesses = session.get('guesses', list())
    if guess.lower() in guesses:
        response_data = {
        "status": "failure",
        'message': "Word already guessed",
        "guess": guess
        }
        return Response(json.dumps(response_data), status=200, mimetype='application/json')
    if guess.lower() not in guesses:
        guesses.append(guess.lower())
        session['guesses'] = guesses
    response_data = {
        "status": "success",
        'message': "Guess recieved",
        "guess": guess
    }
    response_data["score"] = session.get("score",0)
    response_data["result"] = boggle_game.check_valid_word(session["game"], guess)
    return Response(json.dumps(response_data), status=200, mimetype='application/json')

@app.route('/gameover', methods=["POST"])
def game_over():
    """Accepts a POST request with the score of the last game, if this score is higher than the previous highscore in session then it will replace it"""
    data = request.json
    score = data.get("score")
    response_data = {
        "status": "success",
        'message': "Score recieved",
        "score": score
    }
    session['times_played'] = session.get('times_played',0) + 1
    if session.get('highscore',0) < int(score):
        session['highscore'] = int(score)
    return Response(json.dumps(response_data), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=8001)