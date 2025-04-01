create table if not exists goals_silver (
    match_id VARCHAR,
    goal_id VARCHAR,
    scorer VARCHAR,
    scoring_team VARCHAR,
    home_team VARCHAR,
    away_team VARCHAR,
    goal_date DATE,
    goal_minute VARCHAR
    
)