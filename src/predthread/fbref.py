import pandas as pd
import pendulum

def load_schedule_table():
    squad_id = "33c895d4"
    url = f"https://fbref.com/en/squads/{squad_id}"
    return pd.read_html(url)[1]


def get_matchweek(table, i_matchweek):
    return table[table.Round == f"Matchweek {i_matchweek}"]


def home_and_away_team(matchweek):
    opponent = matchweek.Opponent.values[0]
    if matchweek.Venue.values[0] == "Home":
        return "Southampton", opponent
    else:
        return opponent, "Southampton"


def match_time_us_central(matchweek):
    uk_timezone = pendulum.timezone('Europe/London')
    us_central = pendulum.timezone("US/Central")
    y, m, d = [int(x) for x in matchweek.Date.values[0].split("-")]
    h, min = [int(x) for x in matchweek.Time.values[0].split(":")]
    return pendulum.datetime(y, m, d, h, min, tz=uk_timezone).astimezone(us_central)


def match_metadata(i_matchweek):
    matchweek = get_matchweek(load_schedule_table(), i_matchweek)
    home_team, away_team = home_and_away_team(matchweek)
    dt = match_time_us_central(matchweek)
    return f'''
{i_matchweek} : {{ 
    "HomeTeam": "{home_team}",
    "AwayTeam": "{away_team}",
    "MatchResult": pt.MatchResult(0, 0),
    "MatchTime": datetime({dt.year}, {dt.month}, {dt.day}, {dt.hour}, {dt.minute}),
    "URL": "",
}}'''