import requests
import time
import json
from secrets import CLIENT_ID, OAUTH_TOKEN

def get_all_covers():
    url = 'https://api.igdb.com/v4/covers'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {OAUTH_TOKEN}'
    }
    covers = []
    limit = 500
    offset = 0
    while offset < 500000:
        query = f'fields *; where id >= {offset} & id < {offset + limit}; limit 500;'
        response = requests.post(url, headers=headers, data=query)
        response.raise_for_status()
        game_set = response.json()
        covers.extend(game_set)
        offset += limit
        print(f"Retrieved {len(game_set)} covers; Total so far: {len(covers)}")
        time.sleep(0.30)
    return covers

covers = get_all_covers()
with open('igdb_covers.json', 'w') as file:
    json.dump(covers, file, indent=4)
print(f"Saved {len(covers)} covers to igdb_covers.json")