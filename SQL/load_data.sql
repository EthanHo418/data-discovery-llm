truncate item;
truncate matches;
truncate participants;
truncate trait;
truncate unit;

\copy item            from ~/projects/data-discovery-llm/data/csv/items.csv header csv;
\copy matches         from ~/projects/data-discovery-llm/data/csv/matches.csv header csv;
\copy participants    from ~/projects/data-discovery-llm/data/csv/participants.csv header csv;
\copy trait           from ~/projects/data-discovery-llm/data/csv/traits.csv header csv;
\copy unit            from ~/projects/data-discovery-llm/data/csv/units.csv header csv;
