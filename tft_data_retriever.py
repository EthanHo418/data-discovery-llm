import requests


response = requests.get("https://devloper.riotgames.com/docs/portal")

print(response.status_code)