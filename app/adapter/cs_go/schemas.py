from typing import TypedDict

from pydantic import BaseModel


class StatsPossibles(TypedDict):
    Played: int
    Won: int
    Lost: int
    Tied: int
    Kills: int
    Deaths: int
    Assists: int
    Headshots: int
    Damage: int
    Rounds: int


class CsStatsInfoSchema(BaseModel):
    name: str
    wins: int
    losses: int
    ties: int
    rank: int
    best_rank: int
    kills: int
    deaths: int
    assists: int
    headshots: int
    damage: int
