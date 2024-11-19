import sys
import os
from flask import Flask, render_template
import json

# Add the current directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api_clients.get_covers import get_all_covers
from api_clients.get_games import get_all_games
from api_clients.get_keywords import get_all_keywords
from algorithms.query import get_rankings

app = Flask(__name__)

@app.route('/')
def home():
    with open('api_clients/igdb_games.json', 'r') as file:
        games = json.load(file)
    
    with open('api_clients/igdb_covers.json', 'r') as file:
        covers = json.load(file)

    # IDs of the games to feature
    featured_game_ids = [136879, 302156, 119133]
    
    # Find games by ID
    featured_games = [game for game in games if game['id'] in featured_game_ids]
    
    # Attach the cover URL to each game
    for game in featured_games:
        cover = next((c for c in covers if 'game' in c and c['game'] == game['id']), None)
        game['cover_url'] = f"https:{cover['url'].replace('t_thumb', 't_cover_big')}" if cover else None
    
    # Pass the featured games to the template
    return render_template('index.html', featured_games=featured_games)


@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
