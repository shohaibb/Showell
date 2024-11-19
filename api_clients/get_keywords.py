import requests
import time
import json
from config import CLIENT_ID, OAUTH_TOKEN

def get_all_keywords():
    url = 'https://api.igdb.com/v4/keywords'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {OAUTH_TOKEN}'
    }
    data = []
    limit = 1000
    offset = 0
    while True:
        query = f'fields name; where id >= {offset} & id < {offset + limit}; limit 500;'
        response = requests.post(url, headers=headers, data=query)
        response.raise_for_status()
        data_set = response.json()
        if not data_set:
            break
        data.extend(data_set)
        offset += limit
        print(f"Retrieved {len(data_set)}; Total so far: {len(data)}")
        time.sleep(0.30)
    return data

# keywords = get_all_keywords()
# with open('igdb_keywords.json', 'w') as file:
#     json.dump(keywords, file, indent=4)
# print(f"Saved {len(keywords)} keywords to igdb_keywords.json")
