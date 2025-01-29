truncate item;
truncate matches;
truncate participants;
truncate trait;
truncate unit;

\copy item            from    items.csv header csv;
\copy matches         from    matches.csv header csv;
\copy participants    from    participants.csv header csv;
\copy trait           from    traits.csv header csv;
\copy unit            from    units.csv header csv;
