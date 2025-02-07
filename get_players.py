from tft import data_store
import tft
import json

# get players by tier and division
# loop through players and insert into database

connection = data_store.get_connection("dbname=tft user=meatthunder host=localhost password= port=5432")
cursor = connection.cursor()
tft = tft.TFT('RGAPI-7f9c2520-b0ae-4ede-bfbd-03f9a40719c0')

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