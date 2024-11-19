import requests
import time
import json
from config import CLIENT_ID, OAUTH_TOKEN

def get_all_games():
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {OAUTH_TOKEN}'
    }
    games = []
    limit = 500
    offset = 0
    while True:
        query = f'fields *; where id >= {offset} & id < {offset + limit}; limit 500;'
        response = requests.post(url, headers=headers, data=query)
        response.raise_for_status()
        game_set = response.json()
        if not game_set:
            break
        games.extend(game_set)
        offset += limit
        print(f"Retrieved {len(game_set)} games; Total so far: {len(games)}")
        time.sleep(0.30)
    return games

# games = get_all_games()
# with open('igdb_games.json', 'w') as file:
#     json.dump(games, file, indent=4)
# print(f"Saved {len(games)} games to igdb_games.json")