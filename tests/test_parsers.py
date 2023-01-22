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