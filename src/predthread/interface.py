from pathlib import Path
import json
import pandas as pd

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

def standings_after_df(root: Path, match_id: int):
    return pd.read_csv(root / "standings" / f'after-match-{match_id}.csv').sort_values("Points")

def download_predictions(root, match_id: int) -> pd.DataFrame:
    # FOR PREVIOUS WEEK?
    # Get the url for the match id
    # Open the thread
    # Get the predictions
    # Save predictions to csv in proper location
    pass