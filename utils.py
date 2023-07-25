import requests

api_endpoint = "https://www.dnd5eapi.co/api/"

def fetch_resource(endpoint):
    response = requests.get(api_endpoint, endpoint)
    return response.json()