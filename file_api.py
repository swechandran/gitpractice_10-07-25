import requests
from config import HEADERS

def get_file_data(file_id):
    url = f"https://api.figma.com/v1/files/{file_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[ERROR] Failed to fetch file {file_id}. Status: {response.status_code}")
        return None
