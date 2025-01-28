import requests
import json
import os
import csv
from datetime import datetime

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


def get_tft_response(endpoint, **kwargs):
    params = {
        'api_key': API_KEY,
    }
    url = f"{DOMAIN_URL}/{endpoint}"
    url = url.format(**kwargs)
    response = requests.get(url, params=params)
    return response.json()


def persist_matches(gamer_name, tag_line):
    # account_info = get_account_info(gamer_name, tag_line)
    account_info = get_tft_response(
        ACCOUNT_URL,
        **{'gamer_name': gamer_name, 'tag_line': tag_line},
    )
    print(account_info)
    match_ids = get_match_ids(account_info['puuid'])
    stored_match_ids = get_stored_match_ids()
    for match_id in match_ids:
        if match_id in stored_match_ids:
            continue
        match_info = get_match_info(match_id)
        with open(f'data/match/{match_id}.json', 'w') as f:
            f.write(json.dumps(match_info, indent=4))


def parse_match_info(file_path):
    with open(file_path, 'r') as f:
        match_info = json.load(f)
    return match_info


def persist_csv(file_path, data):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    # persist_matches('PPG Rex', 'PPG')
    # persist_matches('StuckStepLaner', 'NA1')
    match_info = parse_match_info('data/match/NA1_5193017032.json')
    match_data = []

    game_datetime = str(datetime.fromtimestamp(match_info['info']['game_datetime'] / 1000))
    match_data.append(
        {
            "match_id": match_info['metadata']['match_id'],
            "game_datetime": game_datetime,
            "game_length": match_info['info']['game_length'],
            "game_version": match_info['info']['game_version'],
            "queue_id": match_info['info']['queue_id'],
            "end_game_result": match_info['info']['endOfGameResult'],
            "game_id": match_info['info']['gameId'],
            "map_id": match_info['info']['mapId'],
        }
    )
    persist_csv('matches.csv', match_data)

    participant_data = []
    for participant in match_info['info']['participants']:
        participant_data.append(
            {
                "match_id": match_info['metadata']['match_id'],
                "puuid": participant['puuid'],
                "gamer_name": participant['riotIdGameName'],
                "tag_line": participant['riotIdTagline'],
                "partner_group_id": participant['partner_group_id'],
                "companion": participant['companion']['species'],
                "gold_left": participant['gold_left'],
                "placement": participant['placement']
            }
        )
    persist_csv('participants.csv', participant_data)
