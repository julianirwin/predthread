"""
Funcitons associated with parsing text into data
"""


import re
from typing import Optional, Sequence, Any
import pandas as pd

from .match_result import MatchResult


def predictions(comments: dict[str, str]) -> pd.DataFrame:
    return pd.DataFrame.from_dict(
        {username: _result_and_comment_dict(comment) for username, comment in comments.items() if _is_valid_comment(comment)}, orient="Index"
    )

def _is_valid_comment(comment: str) -> bool:
    return _first_two_ints_in_comment(comment) is not None


def _result_and_comment_dict(comment: str) -> dict[str, Any]:
    return {"Comment": comment, "Prediction": _predicted_match_result(comment)}


def _predicted_match_result(valid_comment: str) -> MatchResult:
    return MatchResult(*_first_two_ints_in_comment(valid_comment))


def _first_two_ints_in_comment(comment: str) -> Optional[tuple[int]]:
    ints_in_comment = re.findall("(\d+)", comment)
    if len(ints_in_comment) < 2:
        return None
    else:
        return tuple(int(x) for x in ints_in_comment[:2])


def standings(self_text: str) -> dict[str, int]:
    lines = self_text.strip().split("\n")
    return _standings_from_lines(_after_header_line(lines))


def _after_header_line(lines: Sequence[str]) -> Sequence[str]:
    if lines == []:
        return []
    if _is_header_line(lines[0]):
        return lines[2:]
    else:
        return _after_header_line(lines[1:])


def _standings_from_lines(lines: Sequence[str]) -> pd.DataFrame:
    """
    Old Format: author -> points
    New Format author -> points, points_gained, exacts, corrects, guesses
    """
    standings = {}
    for line in lines:
        try:
            author, points = _without_spaces(line).split("|")
            standings[author] = int(points)
        except ValueError:
            author, points, points_gained, exacts, corrects, wrongs = _without_spaces(line).split("|")
            author = _untag_if_needed(author)
            standings[author] = {
                "Points": int(points),
                "PointsGained": int(points_gained),
                "Exacts": int(exacts),
                "Corrects": int(corrects),
                "Wrongs": int(wrongs),
            }
    return pd.DataFrame.from_dict(standings, orient="Index")


def _without_spaces(s):
    return "".join(filter(lambda x: not x.isspace(), s))


def _is_header_line(line):
    return "User|Points" in _without_spaces(line)


def _untag_if_needed(author: str):
    if author.startswith("u/"):
        return author[2:]
    else:
        return author
