from predthread import MatchResult
from pytest import fixture

equal_scores = (
    ((0, 0), (0, 0)),
    ((1, 0), (1, 0)),
    ((0, 1), (0, 1)),
    ((1, 1), (1, 1)),
    ((5, 5), (5, 5)),
)
@fixture(params=equal_scores)
def exactly_equal_match_results(request):
    return MatchResult(*request.param[0]), MatchResult(*request.param[1])

unequal_scores = (
    ((0, 0), (0, 1)),
    ((1, 0), (0, 0)),
    ((1, 1), (0, 0)),
    ((1, 1), (3, 1)),
    ((5, 5), (0, 5)),
)
@fixture(params=unequal_scores)
def not_exactly_equal_match_results(request):
    return MatchResult(*request.param[0]), MatchResult(*request.param[1])

same_result_scores = (
    ((0, 0), (1, 1)),
    ((1, 0), (3, 0)),
    ((2, 2), (0, 0)),
    ((1, 3), (2, 4)),
)
@fixture(params=same_result_scores)
def same_result_match_results(request):
    return MatchResult(*request.param[0]), MatchResult(*request.param[1])

not_same_result_scores = (
    ((0, 0), (2, 1)),
    ((1, 1), (3, 0)),
    ((2, 0), (0, 2)),
    ((1, 3), (4, 4)),
)
@fixture(params=not_same_result_scores)
def not_same_result_match_results(request):
    return MatchResult(*request.param[0]), MatchResult(*request.param[1])

class TestMatchResult:
    def test_init(self):
        match_result = MatchResult(0, 0)

    def test_exactly_equal(self, exactly_equal_match_results):
        mr1, mr2 = exactly_equal_match_results
        assert mr1.exactly_equals(mr2)

    def test_not_exactly_equal(self, not_exactly_equal_match_results):
        mr1, mr2 = not_exactly_equal_match_results
        assert not mr1.exactly_equals(mr2)

    def test_same_result_as(self, same_result_match_results):
        mr1, mr2 = same_result_match_results
        assert mr1.same_result_as(mr2)

    def test_not_same_result_as(self, not_same_result_match_results):
        mr1, mr2 = not_same_result_match_results
        assert not mr1.same_result_as(mr2) 