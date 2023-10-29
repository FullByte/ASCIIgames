from flask import Flask, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def main_menu():
    return '''
        <h1>Please choose an option:</h1>
        <ul>
            <li><a href="/start_einhorn">Start Einhorn</a></li>
            <li><a href="/start_tictactoe">Start TicTacToe</a></li>
        </ul>
    '''

@app.route('/start_einhorn')
def start_einhorn():
    os.chdir('./einhorn')
    subprocess.call(["python", "main.py"])
    os.chdir('..')
    return redirect(url_for('main_menu'))

@app.route('/start_tictactoe')
def start_tictactoe():
    subprocess.call(["python", "./tictactoe/main.py"])
    return redirect(url_for('main_menu'))

if __name__ == "__main__":
    app.run(debug=True)