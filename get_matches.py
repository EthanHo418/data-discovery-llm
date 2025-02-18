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
        if tier == 'DIAMOND' and division == 'I':
            continue
        for queue in queues:
            players = data_store.get_players(cursor, tier, division, queue)
            logger.info(f"{len(players)} for {tier}: {division} - {queue}")
            for i, player in enumerate(players):
                logger.info(f"{i} / {len(players)} players fetched")
                start_time = '2025-02-05 00:00:00'
                end_time = '2025-02-05 23:59:59'
                match_ids = tft.get_match_ids(player['puuid'], start_time, end_time)
                for match_id in match_ids:
                    data_store.set_match(cursor, player['puuid'], match_id)
                connection.commit()
                import sys
                sys.exit()


connection.close()

