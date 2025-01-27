import requests
import json
import os

API_KEY = "RGAPI-57179589-e02c-4645-b464-fdfad4485114"
DOMAIN_URL = "https://americas.api.riotgames.com"
ACCOUNT_URL = "riot/account/v1/accounts/by-riot-id/{gamer_name}/{tag_line}"
MATCH_URL = "tft/match/v1/matches/by-puuid/{puuid}/ids"
MATCH_INFO_URL = "tft/match/v1/matches/{match_id}"


def get_stored_match_ids():
    directory_path = 'data/match/'
    files = os.listdir(directory_path)
    files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
    files = [f.replace('.json', '') for f in files]
    return files


def get_account_info(gamer_name, tag_line):
    params = {
        'api_key': API_KEY,
    }
    full_url = f"{DOMAIN_URL}/{ACCOUNT_URL}"
    full_url = full_url.format(gamer_name=gamer_name, tag_line=tag_line)
    response = requests.get(full_url, params=params)
    return response.json()


def get_match_ids(puuid):
    params = {
        'api_key': API_KEY,
    }
    url = f"{DOMAIN_URL}/{MATCH_URL}"
    url = url.format(puuid=puuid)
    response = requests.get(url, params=params)
    return response.json()


def get_match_info(match_id):
    params = {
        'api_key': API_KEY,
    }
    url = f"{DOMAIN_URL}/{MATCH_INFO_URL}"
    url = url.format(match_id=match_id)
    response = requests.get(url, params=params)
    return response.json()


def persist_matches(gamer_name, tag_line):
    account_info = get_account_info(gamer_name, tag_line)
    match_ids = get_match_ids(account_info['puuid'])
    stored_match_ids = get_stored_match_ids()
    for match_id in match_ids:
        if match_id in stored_match_ids:
            continue
        match_info = get_match_info(match_id)
        with open(f'data/match/{match_id}.json', 'w') as f:
            f.write(json.dumps(match_info, indent=4))


if __name__ == '__main__':
    persist_matches('PPG Rex', 'PPG')
    persist_matches('StuckStepLaner', 'NA1')
