DROP TABLE IF EXISTS trait;
CREATE TABLE trait (
    match_id VARCHAR(255),       -- Unique match identifier
    puuid VARCHAR(255),       -- Unique match identifier
    name VARCHAR(255),       -- Unique match identifier
    num_units INT,
    style INT,
    tier_current INT,
    tier_total INT,
    PRIMARY KEY(match_id, puuid, name)
);