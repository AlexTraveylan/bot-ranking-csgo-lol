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
    "UNRANKED",
    "IRON",
    "BRONZE",
    "SILVER",
    "GOLD",
    "PLATINUM",
    "EMERALD",
    "DIAMOND",
    "MASTER",
    "GRANDMASTER",
    "CHALLENGER",
]

TIER_ORDER = {
    "UNRANKED": 0,
    "IRON": 1,
    "BRONZE": 2,
    "SILVER":  3,
    "GOLD": 4,
    "PLATINUM": 5,
    "EMERALD": 6,
    "DIAMOND": 7,
    "MASTER": 8,
    "GRANDMASTER": 9, 
    "CHALLENGER": 10
}


type Rank = Literal["I", "II", "III", "IV", "UNRANKED"]

RANK_ORDER = {"I": 3, "II": 2, "III": 1, "IV": 0, "UNRANKED": -1}


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

    @classmethod
    def from_no_data(cls):
        return cls(
            leagueId="",
            queueType="",
            tier="UNRANKED",
            rank="UNRANKED",
            summonerId="",
            leaguePoints=0,
            wins=0,
            losses=0,
            veteran=False,
            inactive=False,
            freshBlood=False,
            hotStreak=False,
        )


class LeagueOutput(BaseModel):
    league: list[LeagueOutputItem]
