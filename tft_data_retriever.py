import requests
import json
import os
import csv
from datetime import datetime, timedelta, timezone
import tft


API_KEY = "RGAPI-d76ec4b1-d593-4c4b-933e-32e6cae866d5"
DOMAIN_URL = "https://americas.api.riotgames.com"
ACCOUNT_URL = "riot/account/v1/accounts/by-riot-id/{gamer_name}/{tag_line}"
MATCH_URL = "tft/match/v1/matches/by-puuid/{puuid}/ids"
MATCH_INFO_URL = "tft/match/v1/matches/{match_id}"
TWO_MONTHS_AGO = int((datetime.now(timezone.utc) - timedelta(days=60)).timestamp())  # 2 months ago in UTC
COUNT = 5000

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
        'start': 0,
        'startTime': TWO_MONTHS_AGO,
        'count': COUNT,
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
    if os.path.exists(file_path):
        with open(file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writerows(data)
    else:
        with open(file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


def ingest_match(file_path):
    print(file_path)
    match_info = parse_match_info("data/match/" + file_path)
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

    participant_data = []
    trait_data = []
    unit_data = []
    item_data = []
    for participant in match_info['info']['participants']:
        participant_data.append(
            {
                "match_id": match_info['metadata']['match_id'],
                "puuid": participant['puuid'],
                "gamer_name": participant['riotIdGameName'],
                "tag_line": participant['riotIdTagline'],
                "partner_group_id": None if 'partner_group_id' not in participant else participant['partner_group_id'],
                "companion": participant['companion']['species'],
                "gold_left": participant['gold_left'],
                "placement": participant['placement'],
                "win": participant['win']
            }
        )
        for trait in participant['traits']:
            trait_data.append(
                {
                    "match_id": match_info['metadata']['match_id'],
                    "puuid": participant['puuid'],
                    'name': trait['name'],
                    'num_units': trait['num_units'],
                    'style': trait['style'],
                    'tier_current': trait['tier_current'],
                    'tier_total': trait['tier_total'],
                }
            )
        unit_names = {}
        for unit in participant['units']:
            if unit['character_id'] not in unit_names:
                unit_names[unit['character_id']] = 1
            else:
                unit_names[unit['character_id']] += 1
            unit_data.append(
                {
                    "match_id": match_info['metadata']['match_id'],
                    "puuid": participant['puuid'],
                    'name': unit['character_id'],
                    'identifier': unit_names[unit['character_id']],
                    'rarity': unit['rarity'],
                    'tier': unit['tier'],
                }
            )
            for item in unit['itemNames']:
                item_data.append(
                    {
                        "match_id": match_info['metadata']['match_id'],
                        "puuid": participant['puuid'],
                        'unit_name': unit['character_id'],
                        'identifier': unit_names[unit['character_id']],
                        'name': item,
                    }
                )

    persist_csv('data/csv/matches.csv', match_data)
    persist_csv('data/csv/participants.csv', participant_data)
    persist_csv('data/csv/traits.csv', trait_data)
    persist_csv('data/csv/units.csv', unit_data)
    persist_csv('data/csv/items.csv', item_data)


def get_match_files(directory):
    file_paths = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):  # Ensure it's a file, not a folder
            file_paths.append(filename)
    return file_paths


if __name__ == '__main__':

    file_paths = get_match_files('data/match/')
    for match_file in file_paths:
        ingest_match(match_file)

    persist_matches('PPG Rex', 'PPG')
    #persist_matches('StuckStepLaner', 'NA1')
    #persist_matches('PPG Mirotix', 'NA1')
