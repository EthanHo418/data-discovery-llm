import requests


class TFT:
    DOMAIN_URL = "https://americas.api.riotgames.com"
    NA1_DOMAIN_URL = "https://na1.api.riotgames.com"
    ACCOUNT_URL = "riot/account/v1/accounts/by-riot-id/{gamer_name}/{tag_line}"
    MATCH_URL = "tft/match/v1/matches/by-puuid/{puuid}/ids"
    MATCH_INFO_URL = "tft/match/v1/matches/{match_id}"
    ENTRIES_URL = "tft/league/v1/entries/{tier}/{division}?queue={queue}"

    PAGINATION_COUNT = 5000
    TIERS = [
        'DIAMOND',
        'EMERALD',
        'PLATINUM',
        'GOLD',
        'SILVER',
        'BRONZE',
        'IRON',
    ]

    DIVISIONS = [
        'I',
        'II',
        'III',
        'IV',
    ]

    QUEUES = [
        'RANKED_TFT',
        'RANKED_TFT_DOUBLE_UP',
    ]

    def __init__(self, api_key):
        self._api_key = api_key
        self._headers = {
            "X-Riot-Token": "RGAPI-79b2a035-5e7f-4a52-b7c2-e354104fbf1c",
        }

    def get_tft_response(self, endpoint, **kwargs):
        url = f"{self.NA1_DOMAIN_URL}/{endpoint}"
        url = url.format(**kwargs)
        response = requests.get(url, headers=self._headers)
        return response.json()

    def get_summoners(self, tier, division, queue):
        return self.get_tft_response(
            endpoint=self.ENTRIES_URL,
            **{'tier': tier, 'division': division, 'queue': queue}
        )
