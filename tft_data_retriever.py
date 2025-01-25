import requests


response = requests.get("https://developer.riotgames.com/docs/portal")

print(response.status_code)