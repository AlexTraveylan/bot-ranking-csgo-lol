from typing import Literal

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

type Tier = Literal[
    "IRON",
    "BRONZE",
    "SILVER",
    "GOLD",
    "PLATINUM",
    "DIAMOND",
    "MASTER",
    "GRANDMASTER",
    "CHALLENGER",
]

TIER_ORDER = {
    "IRON": 0,
    "BRONZE": 1,
    "SILVER": 2,
    "GOLD": 3,
    "PLATINUM": 4,
    "DIAMOND": 5,
    "MASTER": 6,
    "GRANDMASTER": 7,
    "CHALLENGER": 8,
}


type Rank = Literal["I", "II", "III", "IV", "V"]

RANK_ORDER = {"I": 4, "II": 3, "III": 2, "IV": 1, "V": 0}


class LeagueOutputItem(BaseModel):
    leagueId: str
    queueType: str
    tier: Tier
    rank: Rank
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
