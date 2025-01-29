truncate item;
truncate matches;
truncate participants;
truncate trait;
truncate unit;

\copy item            from    data/csv/items.csv header csv;
\copy matches         from    data/csv/matches.csv header csv;
\copy participants    from    data/csv/participants.csv header csv;
\copy trait           from    data/csv/traits.csv header csv;
\copy unit            from    data/csv/units.csv header csv;
