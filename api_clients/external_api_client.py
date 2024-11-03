import requests
from config import API_KEY

def fetch_api_data(endpoint, params=None):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()  # Adjust based on the API's response format
