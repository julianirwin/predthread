import pytest
from pytest import fixture

from predthread.parse import _first_two_ints_in_comment, standings
from predthread import MatchResult
import predthread as pt
import pandas as pd
from pandas.testing import assert_frame_equal

__author__ = "Julian"
__copyright__ = "Julian"
__license__ = "MIT"

labelled_comments = (
    ((1, 2), "1 - 2. Saints are going down. Could loose by 8 goals"),
    ((3, 0), "Everton 3 Saints 0. I'm 100% positive."),
    ((3, 0), "Everton 3 Saints 0"),
)


@fixture(params=labelled_comments)
def comment_case(request):
    return {"correct_ints": request.param[0], "comment_text": request.param[1]}


def test_first_two_ints_in_comment(comment_case):
    assert _first_two_ints_in_comment(comment_case["comment_text"]) == comment_case["correct_ints"]


labelled_self_texts_new_format = (
    (
        {
            "mcsgwigga": {"Points": 14, "PointsGained": 3, "Exacts": 4, "Corrects": 2, "Wrongs": 8},
            "BlameTibor": {"Points": 13, "PointsGained": 0, "Exacts": 2, "Corrects": 7, "Wrongs": 9},
            "Seph_che": {"Points": 13, "PointsGained": 1, "Exacts": 3, "Corrects": 4, "Wrongs": 10},
        },
        """
    # Home - Away Format

    Comment like "2 - 1. ⛏️⛏️⛏️"

    Get you  predictions in one hour before kickoff, before lineups are posted.

    # Standings

    User|Points|Earned|Exacts|Corrects|Wrongs
    :--|:--|:--|:--|:--|:--|:--
    mcsgwigga | 14 | 3 | 4 | 2 | 8
    BlameTibor | 13 | 0 | 2 | 7 | 9
    Seph_che | 13 | 1 | 3 | 4 | 10
    """,
    ),
)


@pytest.mark.parametrize("standings_dict,self_text", labelled_self_texts_new_format)
def test_standings_dict_from_self_text_new(standings_dict, self_text):
    assert_frame_equal(standings(self_text), pd.DataFrame.from_dict(standings_dict, orient="Index"))


comments_and_predictions = (
    (
        {
            "rapsin4lmao": "2-0. JWP two direct free kicks to tie Beckham's record.",
            "Zakedawn": "1-3. Reality check",
            "Zou-KaiLi": "0-2 Home curse. Good times can't keep rolling.",
            "ResolutionMoney1390": "4-1. We thoroughly smash Villa, a club which I dislike.",
            "TheDevilishSaint": "1-2. Under Emery I just think they're far better than us. Was actually surprised to see s many predict us to win. Hope for a 2-1 tho.",
            "Salt-Cup-2300": "6-0 all jwp free kicks",
            "gradi3nt": "2 - 1. ⛏️⛏️⛏️",
            "delegod1": "2-1 another silly goal and no clean sheet. NJ goes ballistic over the 6,000th silly goal",
            "MangerDanger1": "Saints 3 - 1 Villa\n\nSend them to the mines",
            "TheFuzzyEucalyptus": "1-2. We also seem to struggle and their fans are always insufferable about it, I don’t suppose this time will be any different.",
            "kyleandrew_7": "3-1",
            "spankeycakes": "2-2",
            "3ch03d": "2-1",
        },
        {
            "rapsin4lmao": (2, 0),
            "Zakedawn": (1, 3),
            "Zou-KaiLi": (0, 2),
            "ResolutionMoney1390": (4, 1),
            "TheDevilishSaint": (1, 2),
            "Salt-Cup-2300": (6, 0),
            "gradi3nt": (2, 1),
            "delegod1": (2, 1),
            "MangerDanger1": (3, 1),
            "TheFuzzyEucalyptus": (1, 2),
            "kyleandrew_7": (3, 1),
            "spankeycakes": (2, 2),
            "3ch03d": (2, 1),
        },
    ),
)


@pytest.mark.parametrize("comments_dict,true_predictions_dict", comments_and_predictions)
def test_parse_predictions(comments_dict, true_predictions_dict):
    test_predictions_df = pt.parse.predictions(comments_dict)
    test_predictions_dict = test_predictions_df["Prediction"].to_dict()
    true_predictions_dict = {author: MatchResult(*prediction_tuple) for author, prediction_tuple in true_predictions_dict.items()}
    assert test_predictions_dict == true_predictions_dict