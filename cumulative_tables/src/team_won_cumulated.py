from datetime import datetime, timedelta
import duckdb


conn = duckdb.connect('../duckdb.sql')

days = 90
starting_date = datetime(2025, 1, 1) - timedelta(days=days)

date_range = [starting_date + timedelta(days=i) for i in range(days)]

with open('../ddl/team_won_cumulated.sql', 'r') as file:
    ddl = file.read()
    conn.query(ddl)

for date in date_range:
    existing_day_str = (date - timedelta(days=1)).strftime("%Y-%m-%d")
    to_add_day_str = date.strftime("%Y-%m-%d")

    sql = f"""

    INSERT INTO team_won_cumulated

    WITH existing AS (
        SELECT * FROM team_won_cumulated
        WHERE snapshot_date = '{existing_day_str}'
    ),

    to_add AS (
        SELECT * FROM team_won_daily
        WHERE match_date = '{to_add_day_str}'
    ),

    combined AS (
        SELECT
            COALESCE(y.team, t.team) AS team,

            COALESCE(
                CASE WHEN array_length(y.wins_array) < 90 THEN
                    [COALESCE(t.did_win, 0)] || y.wins_array
                ELSE
                    [COALESCE(t.did_win, 0)] || list_reverse(list_slice(list_reverse(y.wins_array), 2, 29))
                END,
                [t.did_win]
            ) AS wins_array,

            COALESCE(
                CASE WHEN array_length(y.goals_array) < 90 THEN
                    [COALESCE(t.goals_in_match, 0)] || y.goals_array
                ELSE
                    [COALESCE(t.goals_in_match, 0)] || list_reverse(list_slice(list_reverse(y.goals_array), 2, 29))
                END,
                [t.goals_in_match]
            ) AS goals_array,

            DATE '{to_add_day_str}' AS snapshot_date
        FROM existing y
        FULL OUTER JOIN to_add t ON y.team = t.team
    )

    SELECT
        team,
        wins_array,
        goals_array,
        wins_array[1] AS won_last_match,
        list_sum(list_slice(wins_array, 1, 7)) AS num_wins_7d,
        list_sum(list_slice(goals_array, 1, 7)) AS num_goals_7d,
        list_sum(list_slice(wins_array, 1, 30)) AS num_wins_30d,
        list_sum(list_slice(goals_array, 1, 30)) AS num_goals_30d,
        list_sum(wins_array) AS num_wins_90d,
        list_sum(goals_array) AS num_goals_90d,
        snapshot_date

    FROM combined;

    """

    conn.execute(sql)
