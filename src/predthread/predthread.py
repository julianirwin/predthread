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

default_localtime_cutoff = datetime.datetime(9999, 1, 1, 0, 0, 0)

"""
standings (old):
    dict username: str -> score: int

standings (new):
    dict username: str -> (score: int, points_gained: int, exacts: int, corrects: int, guesses: int)
            standings[author] = tuple(int(x) for x in (points, points_gained, exacts, corrects, guesses))
"""


def get_standings(thread: Submission) -> dict:
    return parse.standings(reddit.thread_self_text(thread))

# Could have this just create a dataframe, that way columns can be easily added and removed, filtered
def get_predictions(thread: Submission, comment_localtime_cutoff: datetime.datetime = default_localtime_cutoff) -> dict:
    comments = reddit.thread_top_level_comments(thread)
    conditions = (comment_filters.comment_author_not_none, comment_filters.comment_created_before(comment_localtime_cutoff))
    valid_comments = comment_filters.filtered_comments(comments, conditions)
    comments_dict = reddit.comments_dict(valid_comments)
    return parse.predictions(comments_dict)


def update_standings_basic(standings: dict[str, int], predictions: dict[str, MatchResult], true_result: MatchResult):
    standings = defaultdict(lambda: 0, standings)
    for author, predicted_result in predictions.items():
        standings[author] = standings[author] + _points_earned(predicted_result, true_result)

def update_standings_detailed(standings, predictions, true_result: MatchResult):
    zero_row = {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 0}
    standings = defaultdict(lambda: zero_row, standings)
    result_type = {0: "Wrongs", 1: "Corrects", 3: "Exacts"}
    for author, predicted_result in predictions.items():
        points_earned = _points_earned(predicted_result, true_result)
        standings[author]["Points"] += points_earned
        standings[author]["PointsGained"] = points_earned
        standings[author][result_type[points_earned]] += 1

def _points_earned(predicted_result: MatchResult, true_result: MatchResult):
        if not predicted_result:
            return 0
        elif predicted_result.exactly_equals(true_result):
            return 3
        elif predicted_result.same_result_as(true_result):
            return 1
        else:
            return 0