select
    b.tier,
    count(1)
from
    participants a
inner join
    player b
    on b.puuid = a.puuid
where
    a.win is True
group by
    b.tier
;


select
    a.puuid,
    count(1)
from
    participants a
join
    player b
    on a.puuid = b.puuid
join
    unit c
    on
where
    a.win is true
group by
    a.puuid
order by
    count(1) desc
;


select
    --count(distinct a.match_id) as match_count,
    --count(distinct a.match_id || b.puuid) as player_match_count,
    --count(distinct a.match_id || b.puuid || c.name || c.identifier) as unit_count
    c.name, d.name, count(1)
from
    matches a
inner join
    participants b
    on a.match_id = b.match_id
inner join
    unit c
    on b.match_id = c.match_id
    and b.puuid = c.puuid
inner join
    item d
    on c.match_id = d.match_id
    and c.puuid = d.puuid
    and c.name = d.unit_name
    and c.identifier = d.identifier
inner join
    player e
    on e.puuid = any(a.puuids)
where
    b.win is true
    and
    c.name = 'tft13_elise'
    and
    e.tier = 'DIAMOND'
group by
    1,2
order by
    3 desc
;