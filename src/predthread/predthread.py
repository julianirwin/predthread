from .reddit import open_reddit, open_thread, thread_self_text, thread_top_level_comments
from .parse import standings, predictions
# import pandas as pd
from praw.reddit import Reddit
from typing import Sequence, Callable

def open_standings_table(reddit: Reddit, url: str) -> dict:
    return standings(thread_self_text(open_thread(reddit, url)))

def get_predictions(reddit: Reddit, url: str) -> dict:
    thread = open_thread(reddit, url) 
    comments = thread_top_level_comments(thread)
    return