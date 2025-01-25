import requests


domain_url = "https://americas.api.riotgames.com"

summoner_name = "PPG Rex"

summoner_url = f"tft/summoner/v1/summoners/by-name/{summoner_name}"

params = {
    "api_key": "RGAPI-839ecb78-0bb6-414d-9eb0-740197ebbc45"
}

response = requests.get(f"{domain_url}/{summoner_url}", params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(response)
    print(response.url)