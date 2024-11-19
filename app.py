import sys
import os
from flask import Flask, render_template

# Add the current directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api_clients.get_covers import get_all_covers
from api_clients.get_games import get_all_games
from api_clients.get_keywords import get_all_keywords
from algorithms.query import get_rankings

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
