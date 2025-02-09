import psycopg2
import json
from datetime import datetime


def get_connection(dsn):
    conn = psycopg2.connect(dsn)
    return conn


def set_player(cursor,  player):
    # insert into player table
    query = f"""
    INSERT INTO player(puuid,  queue,  tier,  division,  api_response) values(%s,  %s,  %s,  %s,  %s)
    """
    cursor.execute(query,  (player['puuid'],  player['queueType'],  player['tier'],  player['rank'],  json.dumps(player)))


def set_match(cursor,  puuid,  match_id):
    query = "select puuids from matches where match_id = %s"
    cursor.execute(query,  (match_id, ))
    row = cursor.fetchone()
    print(row)
    if row:
        if row[0] is None:
            row[0] = []
        if puuid not in row[0]:
            query = "update matches set puuids = %s where match_id = %s"
            cursor.execute(query,  (row[0] + [puuid],  match_id))
    else:
        query = "insert into matches(match_id,  puuids) values (%s,  %s)"
        cursor.execute(query,  (match_id,  [puuid]))


def get_match_ids(cursor):
    query = "SELECT match_id FROM matches where game_datetime is null order by match_id"
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]


def get_players(cursor, tier, division):
    query = "SELECT distinct puuid FROM player WHERE tier = %s and division = %s order by puuid"
    cursor.execute(query, (tier, division))
    return cursor.fetchall()


def set_match_info(cursor,  match_info):
    game_datetime = str(datetime.fromtimestamp(match_info['info']['game_datetime'] / 1000))
    query = f"""
        update
            matches
        set
            game_datetime = %s, 
            game_length = %s, 
            game_version = %s, 
            queue_id = %s, 
            end_game_result = %s, 
            game_id = %s, 
            map_id = %s
        where
            match_id = %s
    """
    cursor.execute(
        query,
        (
            game_datetime,
            match_info['info']['game_length'],
            match_info['info']['game_version'],
            match_info['info']['queue_id'],
            match_info['info']['endOfGameResult'],
            match_info['info']['gameId'],
            match_info['info']['mapId'],
            match_info['metadata']['match_id'],
        )
    )

    for participant in match_info['info']['participants']:
        query = f"""
        insert into
            participants(match_id,  puuid,  game_name,  tag_line,  partner_group,  companion,  gold_left,  placement,  win)
        values
            (%s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s)
        """
        cursor.execute(
            query,  (
                match_info['metadata']['match_id'],
                participant['puuid'],
                participant['riotIdGameName'],
                participant['riotIdTagline'],
                None if 'partner_group_id' not in participant else participant['partner_group_id'],
                participant['companion']['species'],
                participant['gold_left'],
                participant['placement'],
                participant['win']
            )
        )
        for trait in participant['traits']:
            query = f"""
            insert into
                trait(match_id, puuid, name, num_units, style, tier_current, tier_total)
            values
                (%s,  %s,  %s,  %s,  %s,  %s,  %s)
            """
            cursor.execute(
                query,
                (
                    match_info['metadata']['match_id'],
                    participant['puuid'],
                    trait['name'],
                    trait['num_units'],
                    trait['style'],
                    trait['tier_current'],
                    trait['tier_total'],
                )
            )

        unit_names = {}
        for unit in participant['units']:
            query = f"""
            insert into
                unit(match_id, puuid, name, identifier, rarity, tier)
            values
                (%s,  %s,  %s,  %s,  %s,  %s)
            """
            if unit['character_id'] not in unit_names:
                unit_names[unit['character_id']] = 1
            else:
                unit_names[unit['character_id']] += 1
            cursor.execute(
                query,
                (
                    match_info['metadata']['match_id'],
                    participant['puuid'],
                    unit['character_id'],
                    unit_names[unit['character_id']],
                    unit['rarity'],
                    unit['tier'],
                )
            )
            for item in unit['itemNames']:
                query = f"""
                insert into
                    item(match_id, puuid, unit_name, identifier, name)
                values
                    (%s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        match_info['metadata']['match_id'],
                        participant['puuid'],
                        unit['character_id'],
                        unit_names[unit['character_id']],
                        item,
                    )
                )
