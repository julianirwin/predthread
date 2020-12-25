import praw
from pprint import pprint
from collections import defaultdict
from matchresult import MatchResult
from typing import Dict

class PredictionThread:
    def __init__(self, url: str, reddit: ):
        self._thread = reddit.submission(url=url)
    
    def standings(self) -> Dict[str, int]:
        return self._parse_comments()

    def _strip_alphas(self, s):
        return ''.join(list(filter(lambda x: (not x.isalpha()), s)))

    def _parse_comments(self):
        """{author: MatchResult}"""
        predictions = {}
        for top_level_comment in self._thread.comments:
            predictions[top_level_comment.author.name] = self._extract_prediction_from(top_level_comment.body)
        return predictions
            
    def _extract_prediction_from(self, comment_body):
        home_away_pattern = "(\d+)\s*-?\s*(\d+)"
        match = re.search(home_away_pattern, self._strip_alphas(comment_body))
        if match:
            return MatchResult(*map(int, match.groups()))
        else:
            return None

def to_list_sort_by_points(standings):
    return sorted(standings.items(), key=lambda x: x[1])[::-1]
    
def format_standings_list(standings_list):
    header = "User|Points\n:--|:--|:--\n"
    rows = ''.join([f"{author} | {points}\n" for author, points in standings_list])
    return header + rows

def without_spaces(s):
    return ''.join(filter(lambda x: not x.isspace(), s))

def is_header_line(line):
    return "User|Points" in without_spaces(line)

def markdown_to_standings(markdown_string):
    lines = markdown_string.split("\n")
    return standings_from_lines(after_header_line(lines))

def after_header_line(lines):
    if lines == []:
        return []
    if is_header_line(lines[0]):
        return lines[2:]
    else:
        return after_header_line(lines[1:])

def standings_from_lines(lines):
    standings = {}
    for line in lines:
        author, points = without_spaces(line).split('|')
        standings[author] = int(points)
    return standings

def points_from_results(predicted, true):
    if predicted.exactly_equals(true):
        return 3
    elif predicted.same_result_as(true):
        return 1
    else:
        return 0

def update_standings(standings, predictions, true_result):
    """
    standings {author: points}
    predictions {author: MatchResult}
    true_result MatchResult
    """
    standings = defaultdict(lambda: 0, standings)
    for author, match_result in predictions.items():
        standings[author] = standings[author] + points_from_results(predicted=match_result, true=true_result)
    return dict(standings)