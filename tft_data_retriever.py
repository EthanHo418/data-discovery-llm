import requests
import json

puuid = "8yHT2Wp4TM61Xwiw3l5vElIHVqMsiiHYyZeN5tssiye8eTtqzfpjqOGJvu-mez_4mVMKbi4b1fwGEQ"

domain_url = "https://americas.api.riotgames.com"

summoner_name = "PPG+Rex"

summoner_url = f"tft/summoner/v1/summoners/by-name/{summoner_name}"

match_url = f"tft/match/v1/matches/by-puuid/{puuid}/ids"



params = {
    "api_key": "RGAPI-e1c58978-31b8-4c02-b401-3e13fa388b4b"
}

match_hist_response = requests.get(f"{domain_url}/{match_url}", params=params)

match_hist =  match_hist_response.json()
match_id = match_hist[0]
match_info_url = f"tft/match/v1/matches/{match_id}"
response = requests.get(f"{domain_url}/{match_info_url}", params=params)

if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
else:
    print(response)
    print(response.url)
    print("https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/8yHT2Wp4TM61Xwiw3l5vElIHVqMsiiHYyZeN5tssiye8eTtqzfpjqOGJvu-mez_4mVMKbi4b1fwGEQ/ids?start=0&count=20&api_key=RGAPI-e1c58978-31b8-4c02-b401-3e13fa388b4b")