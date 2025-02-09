from tft import data_store
import tft
from dotenv import load_dotenv
import os

load_dotenv()

import json

# get players by tier and division
# loop through players and insert into database

API_KEY = os.environ['API_KEY']
DB_URL = os.environ['DB_URL']

if __name__ == '__main__':
    connection = data_store.get_connection(DB_URL)
    cursor = connection.cursor()
    tft = tft.TFT(API_KEY)

    tiers = ['DIAMOND', 'EMERALD', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
    divisions = ['I', 'II', 'III', 'IV']
    queues = ['RANKED_TFT', 'RANKED_TFT_DOUBLE_UP']

    for tier in tiers:
        for division in divisions:
            for queue in queues:
                players = tft.get_summoners(tier, division, queue, 1)
                for player in players:
                    data_store.set_player(cursor, player)

    connection.commit()
    connection.close()
    #
    # for player in players:
            #     data_store.set_player(cursor, player)
            #
            # connection.commit()