import pandas as pd
import pendulum

def load_schedule_table():
    squad_id = "33c895d4"
    url = f"https://fbref.com/en/squads/{squad_id}"
    table = pd.read_html(url)[1]
    if not "Round" in table.columns:
        table = pd.read_html(url)[0]
        if not "Round" in table.columns:
            raise ValueError("Could not find schedule table on fbref")
    return table


def get_matchweek(table, i_matchweek):
    return table[table.Round == f"Matchweek {i_matchweek}"]


def home_and_away_team(matchweek):
    opponent = matchweek.Opponent.values[0]
    if matchweek.Venue.values[0] == "Home":
        return "Southampton", opponent
    else:
        return opponent, "Southampton"


def match_time_utc(matchweek):
    y, m, d = [int(x) for x in matchweek.Date.values[0].split("-")]
    h, min = [int(x) for x in matchweek.Time.values[0].split(":")]
    return pendulum.datetime(y, m, d, h, min).in_timezone("UTC")


def match_metadata(i_matchweek):
    matchweek = get_matchweek(load_schedule_table(), i_matchweek)
    home_team, away_team = home_and_away_team(matchweek)
    dt = match_time_utc(matchweek)
    return {
        "MatchWeek": i_matchweek,
        "HomeClub": f"{home_team}",
        "AwayClub": f"{away_team}",
        "HomeGoals": "",
        "AwayGoals": "",
        "MatchTimeUtc": dt.to_iso8601_string(),
        "ThreadUrl": "",
    }