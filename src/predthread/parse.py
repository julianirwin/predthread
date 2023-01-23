"""
Funcitons associated with parsing text into data
"""


import re
from typing import Optional, Sequence, Any

from .match_result import MatchResult


def predictions(comments: dict[str, str]):
    return {username: _predicted_match_result(comment) for username, comment in comments.items()}


def _predicted_match_result(comment: str) -> MatchResult:
    return MatchResult(*_first_two_ints_in_comment(comment))


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


def _standings_from_lines(lines: Sequence[str]) -> dict[str, Any]:
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
            standings[author] = {
                "Points": int(points),
                "PointsGained": int(points_gained),
                "Exacts": int(exacts),
                "Corrects": int(corrects),
                "Wrongs": int(wrongs),
            }
    return standings


def _without_spaces(s):
    return "".join(filter(lambda x: not x.isspace(), s))


def _is_header_line(line):
    return "User|Points" in _without_spaces(line)
