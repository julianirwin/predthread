import praw
from pprint import pprint
from collections import defaultdict
from .matchresult import MatchResult
import re
from typing import Dict, Sequence, Tuple
from tabulate import tabulate


class PredictionThread:
    def __init__(
        self,
        home_goals: int,
        away_goals: int,
        saints_are_home: bool,
        url: str,
        client_id: str,
        client_secret: str,
        user_agent: str,
    ):
        self._reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )
        self._thread: praw.models.reddit.submission.Submission = (
            self._reddit.submission(url=url)
        )
        self._home_goals = home_goals
        self._away_goals = away_goals
        self._saints_are_home = saints_are_home

    def predictions(self) -> Dict[str, MatchResult]:
        return self._parse_comments()

    def standings(self) -> Dict[str, int]:
        return self._markdown_to_standings(self._thread.selftext)

    def updated_standings(self, nonzero=False) -> Dict[str, int]:
        true_result = MatchResult(self._home_goals, self._away_goals)
        return self._updated_standings(
            self.standings(), self.predictions(), true_result, nonzero
        )

    def standings_as_markdown(self):
        return self._format_standings_as_markdown(self.standings())

    def updated_standings_as_markdown(self, nonzero=False):
        return self._format_standings_as_markdown(self.updated_standings(nonzero))

    def standings_predictions_updates_table(self, nonzero=False):
        standings = defaultdict(lambda: 0, self.standings())
        predictions = defaultdict(lambda: None, self.predictions())
        updated_standings = self.updated_standings(nonzero)
        table = []
        for a in updated_standings.keys():
            table.append(
                (
                    a,
                    standings[a],
                    predictions[a],
                    updated_standings[a] - standings[a],
                    updated_standings[a],
                )
            )
        return sorted(table, key=lambda x: x[4])[::-1]

    def standings_predictions_updates_table_tabulated(self, nonzero=False):
        table_body = self.standings_predictions_updates_table(nonzero)
        headers = ["User", "Standings", "Prediction", "Earned", "Updated Standings"]
        return tabulate(table_body, headers=headers)

    def compare_to_next_week(self, next_week_url, nonzero=False):
        table_this_week = self.standings_predictions_updates_table(nonzero=nonzero)
        thread_next_week = self._reddit.submission(url=next_week_url)
        standings_next_week = self._markdown_to_standings(thread_next_week.selftext)
        table_this_week = {row[0]: row[1:] for row in table_this_week}
        for author, points in standings_next_week.items():
            table_this_week[author] = table_this_week[author] + (
                points,
                points == table_this_week[author][-1],
            )
        table = [(k, *v) for k, v in table_this_week.items()]
        return table

    def compare_to_next_week_tabulated(self, next_week_url, nonzero=False):
        table_body = self.compare_to_next_week(next_week_url, nonzero)
        headers = ["User", "Standings", "Prediction", "Earned", "Updated Standings", "Standings (Next Weeks Thread)", "Match?"]
        return tabulate(table_body, headers=headers)

    def _strip_alphas(self, s):
        return "".join(list(filter(lambda x: (not x.isalpha()), s)))

    def _parse_comments(self):
        """{author: MatchResult}"""
        predictions = {}
        for top_level_comment in self._thread.comments:
            if top_level_comment.author is None:
                continue
            predictions[top_level_comment.author.name] = self._extract_prediction_from(
                top_level_comment.body,
                self._saints_are_home
            )
        return predictions

    def _extract_prediction_from(self, comment_body, saints_are_home):
        # home_away_pattern = "(\d+)\s*-?\s*(\d+)"
        # match = re.search(home_away_pattern, self._strip_alphas(comment_body))
        # if match:
        #     return MatchResult(*map(int, match.groups()))
        # else:
        #     return None
        s = comment_body.lower()
        reverse_if_saints_away = 1 if saints_are_home else -1

        # Catches the <team1> <score1> <team2> <score2> used by those who don't trust that
        # the game organizer can figure out home - away without labels...      
        reverse_explicit_pattern = "(southampton|saints|us)\s*(\d+)\s*-?\s*[\w\s]*(\d+)"
        match = re.search(reverse_explicit_pattern, s)
        if match:
            return MatchResult(*(int(match.groups()[1]), int(match.groups()[2]))[::reverse_if_saints_away])

        # Catches the <score1> <team1> <score2> <team2> used by those who don't trust that
        # the game organizer can figure out home - away without labels...
        forward_explicit_pattern = "(\d+)\s*(southampton|saints|us)\s*-?\s*(\d+)"
        match = re.search(forward_explicit_pattern, s)
        if match:
            return MatchResult(*(int(match.groups()[0]), int(match.groups()[2]))[::reverse_if_saints_away])
        
        # Catches the <score> <winner> format commonly used in english
        reversed_pattern = "(\d+)\s*-?\s*(\d+)\s*(saints|southampton|us|win|easy win)"
        match = re.search(reversed_pattern, s)
        if match:
            return MatchResult(*(int(match.groups()[0]), int(match.groups()[1]))[::reverse_if_saints_away])
        
        # Home - away format. As requested!
        home_away_pattern = "(\d+)\s*-?\s*(\d+)"
        match = re.search(home_away_pattern, self._strip_alphas(comment_body))
        if match:
            return MatchResult(*map(int, match.groups()))
        else:
            return None

    def _markdown_to_standings(self, markdown_string: str) -> Dict[str, int]:
        lines = markdown_string.strip().split("\n")
        return self._standings_from_lines(self._after_header_line(lines))

    def _after_header_line(self, lines: Sequence[str]) -> Sequence[str]:
        if lines == []:
            return []
        if self._is_header_line(lines[0]):
            return lines[2:]
        else:
            return self._after_header_line(lines[1:])

    def _standings_from_lines(self, lines: Sequence[str]) -> Dict[str, int]:
        standings = {}
        for line in lines:
            author, points = self._without_spaces(line).split("|")
            standings[author] = int(points)
        return standings

    def _without_spaces(self, s):
        return "".join(filter(lambda x: not x.isspace(), s))

    def _is_header_line(self, line):
        return "User|Points" in self._without_spaces(line)

    def _sorted_standings_list(self, standings: Dict[str, int]) -> Sequence[tuple]:
        return sorted(standings.items(), key=lambda x: x[1])[::-1]

    def _format_standings_as_markdown(self, standings: Dict[str, int]):
        sorted_standings_list = self._sorted_standings_list(standings)
        header = "User|Points\n:--|:--|:--\n"
        rows = "".join(
            [f"{author} | {points}\n" for author, points in sorted_standings_list]
        )
        return header + rows

    def _points_from_results(self, predicted, true):
        if not predicted:
            return 0
        elif predicted.exactly_equals(true):
            return 3
        elif predicted.same_result_as(true):
            return 1
        else:
            return 0

    def _updated_standings(self, standings, predictions, true_result, nonzero=False):
        """
        standings {author: points}
        predictions {author: MatchResult}
        true_result MatchResult
        """
        standings = defaultdict(lambda: 0, standings)
        for author, match_result in predictions.items():
            standings[author] = standings[author] + self._points_from_results(
                predicted=match_result, true=true_result
            )
        if nonzero:
            standings = {k: v for k, v in standings.items() if v > 0}
        return dict(standings)