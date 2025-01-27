CREATE TABLE participants (
    match_id VARCHAR(50),       -- Unique match identifier
    puuid VARCHAR(50),       -- Unique match identifier
    companion VARCHAR(50),       -- Unique match identifier
    gold_left INT,
    placement INT,
    PRIMARY KEY(match_id, puuid)
);
