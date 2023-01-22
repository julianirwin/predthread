"""
All functions that use PRAW to access reddit or sort through PRAW models.
"""

import datetime
from typing import Sequence
from functools import reduce
from operator import and_
from .api_keys import client_id, client_secret, user_agent
import praw
from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment
from praw.reddit import Reddit


def open_reddit() -> Reddit:
    return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


def open_thread(reddit, url) -> Submission:
    return reddit.submission(url=url)


def thread_self_text(thread) -> str:
    return thread.selftext


def thread_top_level_comments(thread) -> Sequence:
    return thread.comments


def comments_dict(comments: Sequence[Comment]) -> dict[str, str]:
    return {c.author.name: c.body for c in comments}