import os
import logging

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from tft import data_store
from tft import TFT

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

if __name__ == '__main__':
    tft = TFT(API_KEY)

    connection = None
    try:
        connection = data_store.get_connection(DB_URL)
        connection.autocommit = True
        cursor = connection.cursor(cursor_factory=DictCursor)
        match_ids = data_store.get_match_ids(cursor)
        for i, match_id in enumerate(match_ids):
            try:
                logger.info(f"match_id: {match_id} ({i+1}/{len(match_ids)})")
                match_info = tft.get_match_info(match_id, API_KEY)
                if match_info is None:
                    logger.info(f"returning null from api {match_id}" )
                    continue
                data_store.set_match_info(cursor, match_info)
                #connection.commit()
            except psycopg2.errors.UniqueViolation as e:
                pass
    except:
        if connection:
            connection.close()
        import traceback
        traceback.print_exc()
        # if i == 10:
        #     break

