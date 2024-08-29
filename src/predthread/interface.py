from pathlib import Path
import json
import pandas as pd
from .reddit import open_reddit, open_thread, thread_top_level_comments
from .predthread import get_predictions, update_standings
from .match_result import MatchResult
import pendulum

def club_names(root: Path) -> list[str]:
    with open(root / 'club_names.json') as f:
        return json.load(f)["ClubNames"]

def api_keys(root: Path):
    with open(root / 'api_keys.json') as f:
        json_dict = json.load(f)
        return {
            "praw_client_id": json_dict["ClientId"],
            "praw_client_secret": json_dict["ClientSecret"],
            "praw_user_agent": json_dict["UserAgent"],
        }

def match_metadata(root: Path, match_id: str) -> dict:
    with open(root / 'match_metadata.json') as f:
        return json.load(f)["MatchId"][str(match_id)]

def matches_metadata(root: Path) -> list[dict]:
    with open(root / 'match_metadata.json') as f:
        return json.load(f)["MatchId"]

def matches_metadata_df(root: Path) -> pd.DataFrame:
    return pd.DataFrame.from_dict(matches_metadata(root), orient="index")

    
def fbref_match_metadata(root: Path, match_week: id) -> dict:
    pass

def _next_match_id(match_metadata: dict):
    try:
        return str(int(max(match_metadata["MatchId"].keys())) + 1)
    except ValueError:
        return "0"

def append_match_metadata(root: Path, match_metadata: dict):
    df = matches_metadata_df(root)
    match_week = int(match_metadata["MatchWeek"])
    if match_week in list(df["MatchWeek"]):
        raise ValueError(f"Match metadata for MatchWeek {match_week} already exists")
    with open(root / 'match_metadata.json') as f:
        data = json.load(f)
        data["MatchId"][_next_match_id(data)] = match_metadata
    with open(root / 'match_metadata.json', 'w') as f:
        json.dump(data, f, indent=4)

def download_predictions(root, match_id: int) -> pd.DataFrame:
    meta = match_metadata(root, match_id)
    reddit = open_reddit(**api_keys(root))
    thread = open_thread(reddit, meta["ThreadUrl"])
    match_time_string = meta["MatchTimeUtc"]
    match_time = pendulum.parse(match_time_string).in_tz(pendulum.local_timezone()).naive()
    predictions = get_predictions(
        thread=thread, 
        comment_localtime_cutoff=match_time.subtract(hours=1)
    )
    with open(root / "predictions" / f"match-{match_id}.csv", "w") as f:
        predictions.to_csv(f)
    return predictions

def load_predictions(root: Path, match_id: int) -> pd.DataFrame:
    df = pd.read_csv(root / "predictions" / f"match-{match_id}.csv")
    return df.set_index("UserName")

def summarize_predictions(root: Path, match_id: int) -> dict:
    p = load_predictions(root, match_id)
    home_wins = (p.PredictedHomeGoals > p.PredictedAwayGoals).value_counts().get(True, 0)
    away_wins = (p.PredictedHomeGoals < p.PredictedAwayGoals).value_counts().get(True, 0)
    draws = (p.PredictedHomeGoals == p.PredictedAwayGoals).value_counts().get(True, 0)
    return {
        "TotalPredictions": len(p),
        "TotalHomeWinPredictions": home_wins,
        "TotalAwayWinPredictions": away_wins,
        "TotalDrawPredictions": draws,
    }

def load_standings_after(root: Path, match_id: int) -> pd.DataFrame:
    df = pd.read_csv(root / "standings" / f'after-match-{match_id}.csv')
    df = df.sort_values(["Points", "PointsGained", "Exacts", "Streak"])
    return df.set_index("UserName")


def calculate_updated_standings_after(root: Path, match_id: int):
    if match_id == 0:
        standings = pd.DataFrame()
    else:
        standings = load_standings_after(root, match_id - 1)
    meta = match_metadata(root, match_id)
    true_result = MatchResult(int(meta["HomeGoals"]), int(meta["AwayGoals"]))
    predictions = load_predictions(root, match_id)
    new_standings = update_standings(standings, predictions, true_result)
    new_standings.to_csv(root / "standings" / f'after-match-{match_id}.csv')
    return new_standings

def summarize_standings_after(root: Path, match_id: int) -> dict:
    standings = load_standings_after(root, match_id)
    points_gained_counts = standings.PointsGained.value_counts()
    return {
        "TotalExacts": points_gained_counts.get(3, 0),
        "TotalCorrects": points_gained_counts.get(1, 0),
    }