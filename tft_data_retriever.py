import requests

puuid = "8yHT2Wp4TM61Xwiw3l5vElIHVqMsiiHYyZeN5tssiye8eTtqzfpjqOGJvu-mez_4mVMKbi4b1fwGEQ"

domain_url = "https://americas.api.riotgames.com"

summoner_name = "PPG+Rex"

summoner_url = f"tft/summoner/v1/summoners/by-name/{summoner_name}"

match_url = f"tft/match/v1/matches/by-puuid/{puuid}/ids"

params = {
    "api_key": "RGAPI-839ecb78-0bb6-414d-9eb0-740197ebbc45"
}

response = requests.get(f"{domain_url}/{match_url}", params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(response)
    print(response.url)
    print("https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/8yHT2Wp4TM61Xwiw3l5vElIHVqMsiiHYyZeN5tssiye8eTtqzfpjqOGJvu-mez_4mVMKbi4b1fwGEQ/ids?start=0&count=20&api_key=RGAPI-e1c58978-31b8-4c02-b401-3e13fa388b4b")