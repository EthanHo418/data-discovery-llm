drop table if exists participants;
CREATE TABLE participants (
    match_id VARCHAR(255),       -- Unique match identifier
    puuid VARCHAR(255),       -- Unique match identifier
    game_name varchar(255),
    tag_line varchar(255),
    partner_group INT,
    companion VARCHAR(255),       -- Unique match identifier
    gold_left INT,
    placement INT,
    win BOOLEAN,
    PRIMARY KEY(match_id, puuid)
);
