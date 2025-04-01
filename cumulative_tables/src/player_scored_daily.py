import duckdb
conn = duckdb.connect('duckdb.sql')

with open('../ddl/goals_daily.sql', 'r') as file:
    ddl = file.read()
    conn.query(ddl)


sql = """
    INSERT INTO goals_daily
        SELECT
            scorer,
                -- If the scorer has at least 1 row, they scored in this match
            IF(COUNT(scorer) > 0, 1, 0) as scored_in_match,
            count() as goals_in_match,
            goal_date as match_date

        FROM goals_silver
        GROUP BY scorer, goal_date

"""


conn.execute(sql)
