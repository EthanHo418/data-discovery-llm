import requests
import json
import os

api_key = "RGAPI-57179589-e02c-4645-b464-fdfad4485114"

def get_stored_match_ids():
    directory_path = 'data/match/'
    files = os.listdir(directory_path)
    files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
    files =[f.replace('.json', '') for f in files]
    return files



retrieved_matches = get_stored_match_ids()

tag_line = 'PPG'
summoner_name = "PPG Rex"

puuid = "DqNKF8vPZ9JKsUhKOQ39ijH2p3w660wHowxqnBPnihBgeHyj4Ws7LS9xlHm2lY9claiP_ztgZcDjDQ"
domain_url = "https://americas.api.riotgames.com"
summoner_url = f"tft/summoner/v1/summoners/by-name/{summoner_name}"
match_url = f"tft/match/v1/matches/by-puuid/{puuid}/ids"
params = {
    "api_key": api_key
}

match_hist_response = requests.get(f"{domain_url}/{match_url}", params=params)

match_hist =  match_hist_response.json()
for match_id in match_hist:
    if match_id in retrieved_matches:
        continue
    match_info_url = f"tft/match/v1/matches/{match_id}"
    response = requests.get(f"{domain_url}/{match_info_url}", params=params)

    if response.status_code == 200:
        with open(f'data/match/{match_id}.json', 'w') as f:
            f.write(json.dumps(response.json(), indent=4))
    else:
        print(response)
        print(response.url)
        print("https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/8yHT2Wp4TM61Xwiw3l5vElIHVqMsiiHYyZeN5tssiye8eTtqzfpjqOGJvu-mez_4mVMKbi4b1fwGEQ/ids?start=0&count=20&api_key=RGAPI-e1c58978-31b8-4c02-b401-3e13fa388b4b")