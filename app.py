import sys
import os
from flask import Flask, render_template, request
import json
from datetime import datetime


# Add the current directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api_clients.get_covers import get_all_covers
from api_clients.get_games import get_all_games
from api_clients.get_keywords import get_all_keywords
from algorithms.query import get_rankings

app = Flask(__name__)

# Opening jsons
with open('api_clients/igdb_games.json', 'r') as file:
    games = json.load(file)

with open('api_clients/igdb_covers.json', 'r') as file:
    covers = json.load(file)

# Assigning covers to games
i = 0
j = 0
games = sorted(games, key=lambda x: x["id"])
covers = [cover for cover in covers if "game" in cover]
covers = sorted(covers, key=lambda x: x["game"])
while i != len(games) and j != len(covers):
    current_game = games[i]
    current_cover = covers[j]
    # Check that game id == cover's game id
    if 'game' not in current_cover:
        j += 1
        continue
    if current_game['id'] == current_cover['game']:
        current_game['cover_url'] = f"https:{current_cover['url'].replace('t_thumb', 't_cover_big')}"
        i += 1
        j += 1
    elif current_game['id'] > current_cover['game']:
        j += 1
    elif current_game['id'] < current_cover['game']:
        i += 1

# Define a genre mapping
GENRE_MAP = {
    2: "Point-and-click",
    4: "Fighting",
    5: "Shooter",
    7: "Music",
    8: "Platform",
    9: "Puzzle",
    10: "Racing",
    11: "Real Time Strategy (RTS)",
    12: "Role-playing (RPG)",
    13: "Simulator",
    14: "Sport",
    15: "Strategy",
    16: "Turn-based Strategy (TBS)",
    24: "Tactical",
    25: "Hack and Slash/Beat 'em up",
    26: "Quiz/Trivia",
    30: "Pinball",
    31: "Adventure",
    32: "Indie",
    33: "Arcade",
    34: "Visual Novel",
    35: "Card & Board Game",
    36: "MOBA",
}

# Sorted lists:

# Alphabetical
GAME_NAME = [ game for game in games if "name" in game ]
sorted_ALPHA = sorted(GAME_NAME, key=lambda x: x["name"])

# Rating
GAME_RATING = [ game for game in games if "total_rating" in game ]
sorted_RATING = sorted(GAME_RATING, key=lambda x: x["total_rating"], reverse=True)

# Release date
GAME_RELEASE = [ game for game in games if "first_release_date" in game and game["first_release_date"] < 1731801600 ]
sorted_RELEASE = sorted(GAME_RELEASE, key=lambda x: x["first_release_date"], reverse=True)
print(len(sorted_RELEASE))

@app.route('/')
def home():
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
    # Sorting logic
    sort_option = request.args.get('sort', 'rating').lower()  # Default to alphabetical
    if sort_option == 'rating':
        games_to_display = sorted_RATING
    elif sort_option == 'release':
        games_to_display = sorted_RELEASE
    else:  # Default to alphabetical
        games_to_display = sorted_ALPHA

    # Pagination setup
    games_per_page = 8
    total_pages = -(-len(games_to_display) // games_per_page)  # Ceiling division
    page = int(request.args.get('page', 1))
    start = (page - 1) * games_per_page
    end = start + games_per_page
    paginated_games = games_to_display[start:end]

    return render_template(
        'browse.html',
        games=paginated_games,
        total_pages=total_pages,
        current_page=page,
        current_sort=sort_option
    )



@app.route('/contact')
def contact():
    return render_template('contact.html')

# Define a game mode mapping
GAME_MODE_MAP = {
    1: "Single-player",
    2: "Multiplayer",
    3: "Co-op",
    4: "Split-screen",
}

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    # Fetch game data
    with open('api_clients/igdb_games.json', 'r') as file:
        games = json.load(file)
    
    with open('api_clients/igdb_covers.json', 'r') as file:
        covers = json.load(file)
    
    # Find the game by ID
    game = next((g for g in games if g['id'] == game_id), None)
    if not game:
        return "Game not found", 404

    # Get cover URL
    cover = next((c for c in covers if 'game' in c and c['game'] == game_id), None)
    game['cover_url'] = f"https:{cover['url'].replace('t_thumb', 't_cover_big')}" if cover else None

    # Convert the release date from Unix timestamp to a readable format
    release_date = game.get("first_release_date", None)
    if release_date:
        release_date = datetime.utcfromtimestamp(release_date).strftime('%B %d, %Y')
    else:
        release_date = "Unknown"

    # Map genre IDs to genre names
    genre_ids = game.get("genres", [])
    genres = [GENRE_MAP.get(genre_id, "Unknown Genre") for genre_id in genre_ids]

    # Map game mode IDs to game mode names
    game_mode_ids = game.get("game_modes", [])
    game_modes = [GAME_MODE_MAP.get(mode_id, f"Mode {mode_id}") for mode_id in game_mode_ids]

    game_data = {
        "name": game.get("name"),
        "summary": game.get("summary", "No summary available."),
        "rating": game.get("aggregated_rating", "No rating available."),
        "release_date": release_date,
        "genres": genres,
        "game_modes": game_modes,
        "cover_url": game['cover_url']
    }

    return render_template('game_detail.html', game=game_data)




if __name__ == '__main__':
    app.run(debug=True)
