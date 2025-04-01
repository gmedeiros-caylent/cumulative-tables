import duckdb
conn = duckdb.connect('duckdb.sql')

sql = """
        SELECT * from team_won_cumulated
        where team = 'Brazil'
        and snapshot_date in (select max(snapshot_date) from team_won_cumulated)
"""


conn.query(sql).show()
