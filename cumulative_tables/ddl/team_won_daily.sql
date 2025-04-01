create table if not exists team_won_daily (
    team VARCHAR,
    did_win INTEGER,
    goals_in_match INTEGER,
    match_date DATE
)