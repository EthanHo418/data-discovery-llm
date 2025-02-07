from psycopg2.extras import DictCursor

from tft import data_store
import tft

# get matches of players from "get_players" by puuid
# loop through matches and insert into database

connection = data_store.get_connection("dbname=tft user=meatthunder host=localhost password= port=5432")
cursor = connection.cursor(cursor_factory=DictCursor)
tft = tft.TFT('RGAPI-7f9c2520-b0ae-4ede-bfbd-03f9a40719c0')


players = data_store.get_players(cursor)
for player in players:
    start_time = '2025-02-01 00:00:00'
    end_time = '2025-02-05 23:59:59'
    match_ids = tft.get_match_ids(player['puuid'], start_time, end_time)
    print(player['puuid'], len(match_ids))
    for match_id in match_ids:
        data_store.set_match(cursor, match_id)

connection.commit()
connection.close()
