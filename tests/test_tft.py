from tft import TFT
import json


def test_get_entries():
    tft = TFT(api_key='RGAPI-79b2a035-5e7f-4a52-b7c2-e354104fbf1c')
    summoners = tft.get_summoners('PLATINUM', 'I', 'RANKED_TFT')
    with open('summoner.json', 'w') as f:
        f.write(json.dumps(summoners, indent=4))
