create or replace table team_won_cumulated (
    team VARCHAR,
    wins_array INTEGER[],
    goals_array INTEGER[],
    won_last_match INTEGER,
    num_wins_7d INTEGER,
    num_goals_7d INTEGER,
    num_wins_30d INTEGER,
    num_goals_30d INTEGER,
    num_wins_90d INTEGER,
    num_goals_90d INTEGER,
    snapshot_date DATE,
)