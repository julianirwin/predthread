from . import parse
from . import reddit
from . import comment_filters
from .match_result import MatchResult

import datetime

# import pandas as pd
from praw.reddit import Reddit
from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment
from typing import Sequence, Callable, Any
from collections import defaultdict
from copy import deepcopy
import pandas as pd

default_localtime_cutoff = datetime.datetime(9999, 1, 1, 0, 0, 0)

"""
standings (old):
    dict username: str -> score: int

standings (new):
    dict username: str -> (score: int, points_gained: int, exacts: int, corrects: int, guesses: int)
            standings[author] = tuple(int(x) for x in (points, points_gained, exacts, corrects, guesses))
"""


def get_standings(thread: Submission) -> pd.DataFrame:
    return parse.standings(reddit.thread_self_text(thread))


def get_predictions(thread: Submission, comment_localtime_cutoff: datetime.datetime = default_localtime_cutoff) -> dict:
    comments = reddit.thread_top_level_comments(thread)
    conditions = (
        comment_filters.comment_author_not_none,
        comment_filters.comment_created_before(comment_localtime_cutoff),
    )
    valid_comments = comment_filters.filtered_comments(comments, conditions)
    comments_dict = reddit.comments_dict(valid_comments)
    return parse.predictions(comments_dict)


def update_standings(standings: pd.DataFrame, predictions: pd.DataFrame, true_result: MatchResult):
    zero_row = {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 0}
    predictions_dict = predictions.to_dict(orient="Index")
    standings_dict = standings.to_dict(orient="Index")
    for k, v in standings_dict.items():
        standings_dict[k]["PointsGained"] = 0
    updated_standings = defaultdict(lambda: deepcopy(zero_row), standings_dict)
    result_type = {0: "Wrongs", 1: "Corrects", 3: "Exacts"}
    for author, prediction in predictions_dict.items():
        points_earned = _points_earned(prediction["Prediction"], true_result)
        updated_standings[author]["Points"] += points_earned
        updated_standings[author]["PointsGained"] = points_earned
        updated_standings[author][result_type[points_earned]] += 1
    return pd.DataFrame.from_dict(updated_standings, orient="Index")


def _points_earned(predicted_result: MatchResult, true_result: MatchResult):
    if not predicted_result:
        return 0
    elif predicted_result.exactly_equals(true_result):
        return 3
    elif predicted_result.same_result_as(true_result):
        return 1
    else:
        return 0
