import requests
import utils
import json
import time
import logging

logger = logging.getLogger(__name__)

from tft_data_retriever import get_tft_response


class TFT:
    DOMAIN_URL = "https://americas.api.riotgames.com"
    NA1_DOMAIN_URL = "https://na1.api.riotgames.com"
    ACCOUNT_URL = "riot/account/v1/accounts/by-riot-id/{gamer_name}/{tag_line}"
    MATCH_URL = "tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}&startTime={start_time}&endTime={end_time}"
    MATCH_INFO_URL = "tft/match/v1/matches/{match_id}"
    ENTRIES_URL = "tft/league/v1/entries/{tier}/{division}?queue={queue}&page={page}"

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
            "X-Riot-Token": api_key,
        }

    def get_tft_response(self, domain, endpoint, **kwargs):
        url = f"{domain}/{endpoint}"
        url = url.format(**kwargs)
        response = requests.get(url, headers=self._headers)
        if response.status_code != 200:
            print(response.url)
        if response.status_code == 429:
            print(json.dumps(response.json(), indent=4))
            logger.info("hit rate limit!")
            for i in range(1, 130):
                time.sleep(1)
                if i % 10 == 0:
                    logger.info(f"sleeping for {i} seconds")
            return self.get_tft_response(domain, endpoint, **kwargs)
        return response.json()

    def get_summoners(self, tier, division, queue, page=1):
        return self.get_tft_response(
            domain=self.NA1_DOMAIN_URL,
            endpoint=self.ENTRIES_URL,
            **{'tier': tier, 'division': division, 'queue': queue, 'page': page}
        )

    def get_match_ids(self, puuid, start_time, end_time):
        start_epoch = utils.to_epoch(start_time)
        end_epoch = utils.to_epoch(end_time)
        return self.get_tft_response(
            domain=self.DOMAIN_URL,
            endpoint=self.MATCH_URL,
            **{'puuid': puuid, 'start_time': start_epoch, 'end_time': end_epoch, 'count': 5000}
        )

    def get_match_info(self, match_id):
        return self.get_tft_response(
            domain=self.DOMAIN_URL,
            endpoint=self.MATCH_INFO_URL,
            **{'match_id': match_id}
        )
