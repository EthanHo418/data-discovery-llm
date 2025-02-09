
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from tft import data_store
import os
import tft

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


tier = 'DIAMOND'
division = 'I'
players = data_store.get_players(cursor, tier, division)
for player in players:
    start_time = '2025-02-05 00:00:00'
    end_time = '2025-02-05 23:59:59'
    match_ids = tft.get_match_ids(player['puuid'], start_time, end_time)
    print(player['puuid'], len(match_ids))
    for match_id in match_ids:
        data_store.set_match(cursor, player['puuid'], match_id)

connection.commit()
connection.close()
