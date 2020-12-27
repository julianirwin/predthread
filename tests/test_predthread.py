from predthread import PredictionThread, MatchResult
from pytest import fixture
from api import client_id, client_secret, user_agent

URL_WEEK14_2020_21 =  "https://www.reddit.com/r/SaintsFC/comments/kf40c7/prediction_thread_week_14/"

EXAMPLE_SELF_TEXT = """
Man City at St. Mary's

Home - Away format

1 point for correct result, 3 points for predicting the final score.

Make your prediction before lineups are released

User	|	Points
:--	|:--	|:--
DrShaftmanPhD	|	13
docdope	|	12
Ik427	|	11
KeepItWavey	|	11
MyoMike	|	11
cbeaz17	|	10
"""
EXAMPLE_SELF_TEXT_STANDINGS = {
    "DrShaftmanPhD": 13,
    "docdope": 12,
    "Ik427": 11,
    "KeepItWavey": 11,
    "MyoMike": 11,
    "cbeaz17": 10
}
EXAMPLE_SELF_TEXT_FORMATTED_OUTPUT = """
User|Points
:--|:--|:--
DrShaftmanPhD | 13
docdope | 12
MyoMike | 11
KeepItWavey | 11
Ik427 | 11
cbeaz17 | 10"""

@fixture(scope="module")
def predthread() -> PredictionThread:
    return PredictionThread(
        url=URL_WEEK14_2020_21,
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

predictions_and_points_params = (
    ((MatchResult(0, 0), MatchResult(0, 0)), 3),
    ((MatchResult(1, 0), MatchResult(1, 0)), 3),
    ((MatchResult(0, 1), MatchResult(0, 1)), 3),
    ((MatchResult(1, 1), MatchResult(1, 1)), 3),
    ((MatchResult(0, 0), MatchResult(1, 1)), 1),
    ((MatchResult(2, 0), MatchResult(4, 1)), 1),
    ((MatchResult(2, 0), MatchResult(2, 5)), 0),
    ((MatchResult(2, 0), MatchResult(3, 3)), 0),
)
@fixture(params=predictions_and_points_params)
def predictions_and_points(request):
    predicted = request.param[0][0]
    true = request.param[0][1]
    points = request.param[1]
    return predicted, true, points

class TestPredictionThread:
    def test_init(self, predthread):
        pass
    
    def test_predictions(self, predthread):
        predictions = predthread.predictions()
        assert predictions['cbeaz17'].exactly_equals(MatchResult(2, 1))
        assert predictions['K3GGY'].exactly_equals(MatchResult(5, 5))
        assert predictions['MyoMike'].exactly_equals(MatchResult(1, 2))
        assert predictions['DrShaftmanPhD'].exactly_equals(MatchResult(2, 1))
        assert predictions['Siteyaself'].exactly_equals(MatchResult(1, 2))
        assert predictions['kyleandrew_7'].exactly_equals(MatchResult(2, 2))
        assert "walterrobot" not in predictions.keys()

    def test_standings(self, predthread):
        standings = predthread.standings()
        assert standings["DrShaftmanPhD"] == 13
        assert standings["cbeaz17"] == 10
        assert standings["MyoMike"] == 11
        assert standings["Siteyaself"] == 6
        assert standings["kyleandrew_7"] == 4
        assert standings["walterrobot"] == 1
        assert 'K3GGY' not in standings.keys()
    
    def test_updated_standings(self, predthread):
        updated_standings = predthread.updated_standings(0, 1)
        assert updated_standings["DrShaftmanPhD"] == 13
        assert updated_standings["cbeaz17"] == 10
        assert updated_standings["MyoMike"] == 12
        assert updated_standings["Siteyaself"] == 7
        assert updated_standings["kyleandrew_7"] == 4
        assert updated_standings["walterrobot"] == 1
        assert updated_standings['K3GGY'] == 0

    def test_table(self, predthread):
        predthread.standings_predictions_updates_table(0, 1)

    def test_table_tabulated(self, predthread):
        predthread.standings_predictions_updates_table_tabulated(0, 1)
    
    def test_example_standings(self, predthread):
        assert predthread._markdown_to_standings(EXAMPLE_SELF_TEXT) == EXAMPLE_SELF_TEXT_STANDINGS

    def test_example_standings_formatted(self, predthread):
        standings = predthread._markdown_to_standings(EXAMPLE_SELF_TEXT)
        formatted_standings_list = predthread._format_standings_as_markdown(standings)
        assert formatted_standings_list.strip() == EXAMPLE_SELF_TEXT_FORMATTED_OUTPUT.strip()
    
    def test_points_from_match_results(self, predthread, predictions_and_points):
        predicted, true, points = predictions_and_points
        assert predthread._points_from_results(predicted, true) == points