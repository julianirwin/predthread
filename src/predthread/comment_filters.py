from typing import Sequence, Callable
from praw.models.reddit.comment import Comment
from functools import reduce
from operator import and_


def comment_author_not_none(comment) -> bool:
    return comment.author is not None


def comment_created_before(threshold_datetime) -> Callable[[Comment], bool]:
    def _comment_created_before(comment):
        comment_time = threshold_datetime.fromtimestamp(comment.created_utc)
        return comment_time <= threshold_datetime

    return _comment_created_before


def filtered_comments(comments: Sequence[Comment], conditions: Sequence[Callable[[Comment], bool]]):
    """
    args are functions that take a comment and return a bool.

    For example:
        filtered_comments(comments, (comment_author_not_none, comment_created_before(datetime_threshold)))
    """

    def f_filter(c):
        return reduce(and_, tuple(f(c) for f in conditions))

    return filter(f_filter, comments)