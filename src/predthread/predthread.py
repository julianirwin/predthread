from . import parse
from . import reddit
from . import comment_filters

import datetime
# import pandas as pd
from praw.reddit import Reddit
from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment
from typing import Sequence, Callable, Any

default_localtime_cutoff = datetime.datetime(9999, 1, 1, 0, 0, 0)


def get_standings(thread: Submission) -> dict:
    return parse.standings(reddit.thread_self_text(thread))


def get_predictions(thread: Submission, comment_localtime_cutoff: datetime.datetime = default_localtime_cutoff) -> dict:
    comments = reddit.thread_top_level_comments(thread)
    conditions = (comment_filters.comment_author_not_none, comment_filters.comment_created_before(comment_localtime_cutoff))
    valid_comments = comment_filters.filtered_comments(comments, conditions)
    comments_dict = reddit.comments_dict(valid_comments)
    return parse.predictions(comments_dict)