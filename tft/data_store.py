import psycopg2
import json

def get_connection(dsn):
    conn = psycopg2.connect(dsn)
    return conn


def set_player(cursor, player):
    # insert into player table
    query = f"""
    INSERT INTO player(puuid, queue, tier, division, api_response) values(%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (player['puuid'], player['queueType'], player['tier'], player['rank'], json.dumps(player)))


def set_match(cursor, match_id):
    # insert into player_matches table
    query = f"""
INSERT INTO matches(match_id) values (%s) ON CONFLICT(match_id) DO NOTHING 
"""
    cursor.execute(query, (match_id, ))


def get_match_ids(cursor):
    query = "SELECT * FROM matches where game_datetime is null"
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]


def get_players(cursor):
    query = "SELECT distinct puuid FROM player order by puuid"
    cursor.execute(query)
    return cursor.fetchall()
