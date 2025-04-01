import duckdb
conn = duckdb.connect('../duckdb.sql')


with open('../ddl/team_won_daily.sql', 'r') as file:
    ddl = file.read()
    conn.query(ddl)


sql = """

    INSERT INTO team_won_daily 
        SELECT
            home_team as team,
            IF(home_score > away_score, 1, 0) as did_win,
            home_score as goals_in_match,
            match_date

        FROM matches_silver
        GROUP BY home_team, home_score, away_score, match_date

        UNION 

        SELECT
            away_team as team,
            IF(away_score > home_score, 1, 0) as did_win,
            away_score as goals_in_match,
            match_date

        FROM matches_silver
        GROUP BY away_team, home_score, away_score, match_date
    

"""


conn.execute(sql)
