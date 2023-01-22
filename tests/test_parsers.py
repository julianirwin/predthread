import pytest

from predthread.parsers import first_two_ints_in_comment, markdown_to_standings

__author__ = "Julian"
__copyright__ = "Julian"
__license__ = "MIT"


def test_first_two_ints_in_comment():
    assert first_two_ints_in_comment("1 - 2. Saints are going down. Could loose by 8 goals") == ["1", "2"]


def test_markdown_to_standings():
    markdown_str = """
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
    """
    standings = {
        "mcsgwigga": 14,
        "BlameTibor": 13,
        "Seph_che": 13,
        "Cervix-Pounder": 12,
        "Zou-KaiLi": 12,
        "TheFuzzyEucalyptus": 11,
        "oldredstang66": 11,
        "lakermamba1999": 10,
    }
    assert markdown_to_standings(markdown_str) == standings