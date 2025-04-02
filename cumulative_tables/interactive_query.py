import duckdb
conn = duckdb.connect('duckdb.sql')

sql = """
        SELECT * from team_won_cumulated
        where team = 'Brazil'
        and
        snapshot_date BETWEEN '2024-10-10' and '2024-10-15'  
"""


conn.query(sql).show()
