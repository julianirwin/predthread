import re
from typing import Optional, Sequence


def first_two_ints_in_comment(comment: str) -> Optional[tuple[int]]:
    ints_in_comment = re.findall("(\d+)", comment)
    if len(ints_in_comment) < 2:
        return None
    else:
        return ints_in_comment[:2]


def markdown_to_standings(markdown_string: str) -> dict[str, int]:
    lines = markdown_string.strip().split("\n")
    return _standings_from_lines(_after_header_line(lines))


def _after_header_line(lines: Sequence[str]) -> Sequence[str]:
    if lines == []:
        return []
    if _is_header_line(lines[0]):
        return lines[2:]
    else:
        return _after_header_line(lines[1:])


def _standings_from_lines(lines: Sequence[str]) -> dict[str, int]:
    standings = {}
    for line in lines:
        author, points = _without_spaces(line).split("|")
        standings[author] = int(points)
    return standings


def _without_spaces(s):
    return "".join(filter(lambda x: not x.isspace(), s))


def _is_header_line(line):
    return "User|Points" in _without_spaces(line)
