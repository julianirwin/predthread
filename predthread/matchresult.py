import enum
import re

class MatchResultEnum(enum.Enum):
    HOME_WIN = 0
    DRAW = 1
    AWAY_WIN = 2

class MatchResult:
    def __init__(self, home_goals, away_goals):
        self.home_goals = home_goals
        self.away_goals = away_goals
    
    def exactly_equals(self, match_result):
        home_goals_equal =  self.home_goals == match_result.home_goals
        away_goals_equal =  self.away_goals == match_result.away_goals
        return home_goals_equal and away_goals_equal
    
    def same_result_as(self, match_result):
        return self.result() == match_result.result()
        
    def result(self):
        if self.home_goals == self.away_goals:
            return MatchResultEnum.DRAW
        if self.home_goals > self.away_goals:
            return MatchResultEnum.HOME_WIN
        if self.home_goals < self.away_goals:
            return MatchResultEnum.AWAY_WIN
    
    def as_tuple(self):
        return (self.home_goals, self.away_goals)
    
    def __repr__(self):
        return "<MatchResult " + str(self.as_tuple()) + " >"

    def __str__(self):
        return str(self.as_tuple())