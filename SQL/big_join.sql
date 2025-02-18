CREATE TABLE tft_analytics AS
SELECT
    a.tier,
    a.division,
    a.queue,
    a.puuid,
    b.match_id,
    c.win,
    c.game_name,
    c.placement,
    c.gold_left,
    c.companion,
    d.name as trait_name,
    d.num_units,
    d.tier_current,
    d.tier_total,
    e.name as unit_name,
    e.identifier,
    e.rarity,
    f.name as item_name
FROM
    player a
JOIN
    matches b
    ON a.puuid = ANY(b.puuids)
JOIN
    participants c
    ON b.match_id = c.match_id
JOIN
    trait d
    ON c.match_id = d.match_id
    AND c.puuid = d.puuid
JOIN
    unit e
    ON d.match_id = e.match_id
    AND d.puuid = e.puuid
JOIN
    item f
    ON e.match_id = f.match_id
    AND e.puuid = f.puuid
    AND e.identifier = f.identifier
    AND e.name = f.unit_name
;

CREATE INDEX player_puuid ON player (puuid);
CREATE INDEX idx_matches_puuids ON matches USING gin (puuids);
CREATE INDEX participants_match_id ON participants(match_id, puuid);
CREATE INDEX trait_match_id ON trait(match_id, puuid);
CREATE INDEX unit_match_id ON unit(match_id, puuid);
CREATE INDEX item_match_id ON item(match_id, puuid, identifier, unit_name);

