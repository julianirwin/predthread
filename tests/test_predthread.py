import pytest
import predthread as pt

predictions_and_detailed_standings = (
    (
        pt.MatchResult(1, 1),
        {
            "user_name_1": pt.MatchResult(0, 0),
        },
        {},
        {
            "user_name_1": {"Points": 1, "PointsGained": 1, "Exacts": 0, "Corrects": 1, "Wrongs": 0},
        },
    ),
    (
        pt.MatchResult(2, 0),
        {
            "user_name_1": pt.MatchResult(2, 0),
        },
        {
            "user_name_1": {"Points": 1, "PointsGained": 1, "Exacts": 0, "Corrects": 1, "Wrongs": 0},
        },
        {
            "user_name_1": {"Points": 4, "PointsGained": 3, "Exacts": 1, "Corrects": 1, "Wrongs": 0},
        },
    ),
    (
        pt.MatchResult(1, 1),
        {
            "mcsgwigga": pt.MatchResult(0, 0),
            "BlameTibor": pt.MatchResult(2, 1),
            "Seph_che":  pt.MatchResult(0, 3),
            "gradi3nt": pt.MatchResult(1, 1)
        },
        {
            "mcsgwigga": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 0},
            "BlameTibor": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 0},
            "Seph_che": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 0},
            "gradi3nt": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 0}
        },
        {
            "mcsgwigga": {"Points": 1, "PointsGained": 1, "Exacts": 0, "Corrects": 1, "Wrongs": 0},
            "BlameTibor": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 1},
            "Seph_che": {"Points": 0, "PointsGained": 0, "Exacts": 0, "Corrects": 0, "Wrongs": 1},
            "gradi3nt": {"Points": 3, "PointsGained": 3, "Exacts": 1, "Corrects": 0, "Wrongs": 0},
        },
    ),
)

@pytest.mark.parametrize("true_result,predictions,standings,updated_standings", predictions_and_detailed_standings)
def test_update_detailed_standings(true_result, predictions, standings, updated_standings):
    assert pt.update_standings_detailed(standings, predictions, true_result) == updated_standings

