import pytest
import predthread as pt
import pandas as pd
from pandas.testing import assert_frame_equal

self_text_empty = (
"""
# Standings
User|Points|Earned|Exacts|Corrects|Wrongs
:--|:--|:--|:--|:--|:--|:--
"""
)

self_text = (
"""
# Standings
User|Points|Earned|Exacts|Corrects|Wrongs
:--|:--|:--|:--|:--|:--|:--
user1 | 0 | 0 | 0 | 0 | 1
"""
)

standings_comments_true_results = (
    {
        "self_text": self_text,
        "comments": {"user1": "0-0"},
        "true_result": pt.MatchResult(1, 0),
        "updated_standings": {
            "user1": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 2},
        }
    },
    {
        "self_text": self_text_empty,
        "comments": {"user1": "0-0"},
        "true_result": pt.MatchResult(1, 0),
        "updated_standings": {
            "user1": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 1},
        }
    },
    {
        "self_text": self_text,
        "comments": {"user1": "0-0"},
        "true_result": pt.MatchResult(1, 1),
        "updated_standings": {
            "user1": {"Points": 1, "PointsGained": 1, "Exacts": 0, "Corrects": 1, "Wrongs": 1},
        }
    },
    {
        "self_text": self_text,
        "comments": {"user1": "0-0"},
        "true_result": pt.MatchResult(0, 0),
        "updated_standings": {
            "user1": {"Points": 3, "PointsGained": 3, "Exacts": 1, "Corrects": 0, "Wrongs": 1},
        }
    },
)

@pytest.mark.parametrize("p", standings_comments_true_results)
def test_update_detailed_standings(p):
    standings_df = pt.parse.standings(p["self_text"])
    predictions_df = pt.parse.predictions(p["comments"])
    updated_standings_df = pd.DataFrame.from_dict(p["updated_standings"], orient="Index")
    assert_frame_equal(pt.update_standings(standings_df, predictions_df, p["true_result"]), updated_standings_df)