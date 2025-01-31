drop TABLE if exists matches;
CREATE TABLE matches (
    match_id VARCHAR(50) PRIMARY KEY,       -- Unique match identifier
    game_datetime TIMESTAMP,               -- Timestamp when the game started
    game_length FLOAT,                     -- Duration of the game (in seconds)
    game_version VARCHAR(255),             -- Version of the game
    queue_id INT,                          -- Queue type ID (e.g., ranked, normal)
    end_game_result VARCHAR(50),           -- End result of the game
    game_id BIGINT,                        -- Numeric identifier of the game
    map_id INT                             -- Map identifier
);pp