from predthread import PredictionThread
from pytest import fixture
from api import client_id, client_secret, user_agent

URL_WEEK14_2020_21 =  "https://www.reddit.com/r/SaintsFC/comments/kf40c7/prediction_thread_week_14/"

@fixture
def predthread():
    return PredictionThread(
        url=URL_WEEK14_2020_21,
        client_id=client_id,
        client_secret=client_secret,
        user_agen=user_agent
    )



class TestPredictionThread:
    def test_init(self, predthread):
        pass