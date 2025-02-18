from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from tft import data_store
import os
import tft
import logging


logging.basicConfig(
    filename='get_match_info.log',  # Log file name
    level=logging.DEBUG,  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
)


logger = logging.getLogger(__name__)

load_dotenv()

# get players by tier and division
# loop through players and insert into database

API_KEY = os.environ['API_KEY']
DB_URL = os.environ['DB_URL']

# get matches of players from "get_players" by puuid
# loop through matches and insert into database

connection = data_store.get_connection(DB_URL)
cursor = connection.cursor(cursor_factory=DictCursor)
tft = tft.TFT(API_KEY)

counter = 1

tier = 'DIAMOND'
division = 'I'
tiers = ['DIAMOND', 'EMERALD', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
divisions = ['I', 'II', 'III', 'IV']
queues = ['RANKED_TFT', 'RANKED_TFT_DOUBLE_UP']


for tier in tiers:
    for division in divisions:
        for queue in queues:
            successful_matches = 0
            players = data_store.get_players(cursor, tier, division, queue)
            for i, player in enumerate(players):
                start_time = '2025-02-05 00:00:00'
                end_time = '2025-02-05 23:59:59'
                match_ids = tft.get_match_ids(player['puuid'], start_time, end_time, API_KEY)
                if match_ids is None:
                    continue
                successful_matches += 1
                logger.info(f"{tier}: {division} - {queue} number of matches: {len(match_ids)} , {i}")
                for match_id in match_ids:
                    data_store.set_match(cursor, player['puuid'], match_id)
                connection.commit()
                if successful_matches == 10:
                    break


connection.close()

# https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/--H8F4Cqu1D5-DKIIHXbpTsgRhvuaKEKSDjRRZYXGU0lsdqusdJe5Zil2ZhZYhOoCgnqAYq3rhm3Dw/ids?count=5000&startTime=1738731600&endTime=1738817999&api_key=RGAPI-11602b19-03f6-4f82-977a-9ff2a19c879d
# https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/GDnSvBpoheknmiA9fvUweGIvFjyEGkT9IAJYaExRbrTF4O-R3BqySNt4GRhptF7PEHMpezTS5derPg/ids?start=0&count=20&api_key=RGAPI-11602b19-03f6-4f82-977a-9ff2a19c879d
# https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/EIAVktspMSeUD4CvCYC4tYrTB33Ihngol2UotoqKzrcUvTNxM-CuJdoHA3slyhryowXxYtSCVDHQRA/ids?start=0&count=20&api_key=RGAPI-11602b19-03f6-4f82-977a-9ff2a19c879d
