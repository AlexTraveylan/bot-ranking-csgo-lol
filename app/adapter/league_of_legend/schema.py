from pydantic import BaseModel

# Account route schemas


class RiotAccountInput(BaseModel):
    game_name: str
    tag_line: str = "euw"


class RiotAccountOutput(BaseModel):
    puuid: str
    gameName: str
    tagLine: str


# Summoner route schemas


class SummonerOutput(BaseModel):
    id: str
    accountId: str
    puuid: str
    profileIconId: int
    revisionDate: int
    summonerLevel: int


# League route schemas


class LeagueOutputItem(BaseModel):
    leagueId: str
    queueType: str
    tier: str
    rank: str
    summonerId: str
    leaguePoints: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    freshBlood: bool
    hotStreak: bool


class LeagueOutput(BaseModel):
    league: list[LeagueOutputItem]
