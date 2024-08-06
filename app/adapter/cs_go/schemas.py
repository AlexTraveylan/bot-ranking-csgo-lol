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

    def to_dict_for_db(self, player_id: str) -> dict[str, int | str]:
        return {
            "player_id": player_id,
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
