from __future__ import annotations

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

    def to_dict_for_db(self, steam_id: str) -> dict[str, int | str]:
        return {
            "steam_id": steam_id,
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties,
            "rank": self.rank,
            "best_rank": self.best_rank,
            "kills": self.kills,
            "deaths": self.deaths,
            "assists": self.assists,
            "headshots": self.headshots,
            "damage": self.damage,
        }

    @classmethod
    def from_no_data(cls) -> CsStatsInfoSchema:
        return cls(
            name="Error",
            wins=0,
            losses=0,
            ties=0,
            rank=0,
            best_rank=0,
            kills=0,
            deaths=0,
            assists=0,
            headshots=0,
            damage=0,
        )
