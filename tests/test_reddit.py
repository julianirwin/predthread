import pytest
import predthread as pt
from predthread import reddit

@pytest.fixture(scope="module")
def _reddit():
    return pt.open_reddit()



prediction_thread_urls = (
    "https://www.reddit.com/r/SaintsFC/comments/10hibga/prediction_thread_week_20_southampton_aston_villa/",
)
@pytest.mark.parametrize("url", prediction_thread_urls)
def test_open_thread(_reddit, url):
    reddit.open_thread(_reddit, url)


@pytest.fixture(scope="module")
def a_thread(_reddit):
    return reddit.open_thread(_reddit, prediction_thread_urls[0])


def test_thread_self_text(a_thread):
    reddit.thread_self_text(a_thread)

def test_thread_self_text(a_thread):
    reddit.thread_top_level_comments(a_thread)