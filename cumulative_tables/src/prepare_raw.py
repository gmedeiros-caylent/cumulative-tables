import duckdb

conn = duckdb.connect('../duckdb.sql')

with open('../ddl/goals_silver.sql', 'r') as file:
    ddl = file.read()
    conn.query(ddl)

with open('../ddl/matches_silver.sql', 'r') as file:
    ddl = file.read()
    conn.query(ddl)


conn.execute('delete from matches_silver')
conn.execute('delete from goals_silver')

conn.execute("""
    INSERT INTO matches_silver
    SELECT
        md5( concat_ws('_', date, home_team, away_team) ) as match_id,
        date as match_date, 
        home_team,
        away_team, 
        home_score,
        away_score
    
             
    FROM '../data/bronze/results.csv'
    WHERE date > '1960-01-01'
""")


conn.execute("""
    INSERT INTO goals_silver
    SELECT
        md5( concat_ws('_', date, scorer, home_team, away_team) ) as goal_id,
        md5( concat_ws('_', date, home_team, away_team) ) as match_id,
        scorer,
        team as scoring_team,
        home_team,
        away_team,
        date as goal_date,
        minute as goal_minute
             

    FROM '../data/bronze/goalscorers.csv'
    WHERE date > '1960-01-01'
""")

