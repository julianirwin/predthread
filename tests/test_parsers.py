import pytest
from pytest import fixture

from predthread.parse import _first_two_ints_in_comment, standings

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


labelled_self_texts = (
    (
        {
            "mcsgwigga": 14,
            "BlameTibor": 13,
            "Seph_che": 13,
            "Cervix-Pounder": 12,
            "Zou-KaiLi": 12,
            "TheFuzzyEucalyptus": 11,
            "oldredstang66": 11,
            "lakermamba1999": 10,
        },
        """
    # Home - Away Format

    Comment like "2 - 1. ⛏️⛏️⛏️"

    Get you  predictions in one hour before kickoff, before lineups are posted.

    # Standings

    User|Points
    :--|:--|:--
    mcsgwigga | 14
    BlameTibor | 13
    Seph_che | 13
    Cervix-Pounder | 12
    Zou-KaiLi | 12
    TheFuzzyEucalyptus | 11
    oldredstang66 | 11
    lakermamba1999 | 10
    """,
    ),
)


@pytest.mark.parametrize("standings_dict,self_text", labelled_self_texts)
def test_standings_dict_from_self_text(standings_dict, self_text):
    assert standings(self_text) == standings_dict

labelled_self_texts_new_format = (
    (
        {
            "mcsgwigga": {"Points": 14, "PointsGained": 3, "Exacts": 4, "Corrects": 2, "Wrongs": 8},
            "BlameTibor": {"Points": 13, "PointsGained": 0, "Exacts": 2, "Corrects": 7, "Wrongs": 9},
            "Seph_che": {"Points": 13, "PointsGained": 1, "Exacts": 3, "Corrects": 4, "Wrongs": 10}
        },
        """
    # Home - Away Format

    Comment like "2 - 1. ⛏️⛏️⛏️"

    Get you  predictions in one hour before kickoff, before lineups are posted.

    # Standings

    User|Points
    :--|:--|:--
    mcsgwigga | 14 | 3 | 4 | 2 | 8
    BlameTibor | 13 | 0 | 2 | 7 | 9
    Seph_che | 13 | 1 | 3 | 4 | 10
    """,
    ),
)


@pytest.mark.parametrize("standings_dict,self_text", labelled_self_texts_new_format)
def test_standings_dict_from_self_text_new(standings_dict, self_text):
    assert standings(self_text) == standings_dict