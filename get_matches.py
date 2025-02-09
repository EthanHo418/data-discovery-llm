import time
from psycopg2.extras import DictCursor
from tft import data_store
import tft

# get matches of players from "get_players" by puuid
# loop through matches and insert into database

connection = data_store.get_connection("dbname=tft user=meatthunder host=localhost password= port=5432")
cursor = connection.cursor(cursor_factory=DictCursor)
tft = tft.TFT('RGAPI-7f9c2520-b0ae-4ede-bfbd-03f9a40719c0')

counter = 1

players = data_store.get_players(cursor)
for player in players:
    counter += 1
    start_time = '2025-02-01 00:00:00'
    end_time = '2025-02-01 23:59:59'

    retries = 5
    delay = 2

    while retries > 0:
        try:
            match_ids = tft.get_match_ids(player['puuid'], start_time, end_time)
            print(player['puuid'], len(match_ids), counter)
            for match_id in match_ids:
                data_store.set_match(cursor, match_id)
            break

        except Exception as e:
            print(f"Request failed for {player['puuid']} (attempt {6 - retries}): {e}")
            time.sleep(delay)  # Wait before retrying
            delay *= 2  # Exponential backoff
            retries -= 1
    if retries == 0:
        print(f"Skipping player {player['puuid']} after multiple failures.")

connection.commit()
connection.close()

