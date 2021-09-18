import requests

def get_api(url:str, params:dict):
    result = requests.get(url, params)
    return result.json()