import contextlib
from datetime import datetime
from typing import Self

from pydantic import ConfigDict
from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlmodel import Field, Session, SQLModel

from app.adapter.exception.bot_exception import BotException
from app.adapter.league_of_legend.schema import RANK_ORDER, TIER_ORDER
from app.core.constants import SUPABASE_URL


class BaseSQLModel(SQLModel):
    model_config = ConfigDict(validate_assignment=True)


class DiscordMember(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_id: str = Field(max_length=100, unique=True)
    discord_name: str = Field(max_length=100)

    def __str__(self) -> str:
        return self.discord_name

    def __repr__(self):
        return f"DiscordMember(id={self.id}, discord_id={self.discord_id}, discord_name={self.discord_name})"


class RiotAccount(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_name: str = Field(max_length=100)
    tag_line: str = Field(max_length=100, default="euw")
    puuid: str = Field(max_length=100)
    summoner_id: str = Field(max_length=100)
    discord_member_id: int = Field(
        sa_column=Column(Integer, ForeignKey("discordmember.id", ondelete="CASCADE"))
    )

    def __str__(self):
        return f"{self.game_name}#{self.tag_line}"

    def __repr__(self):
        return f"RiotAccount(game_name={self.game_name}, tag_line={self.tag_line}, puuid={self.puuid}, summoner_id={self.summoner_id}, discord_member_id={self.discord_member_id})"


class RiotScore(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tier: str
    rank: str
    leaguePoints: int
    wins: int
    losses: int
    created_at: datetime = Field(default=datetime.now)
    riot_account_id: int = Field(
        sa_column=Column(Integer, ForeignKey("riotaccount.id", ondelete="CASCADE"))
    )

    def __str__(self):
        return f"{self.tier} {self.rank} {self.leaguePoints} LP"

    def __repr__(self):
        return f"RiotScore(tier={self.tier}, rank={self.rank}, leaguePoints={self.leaguePoints}, wins={self.wins}, losses={self.losses}, created_at={self.created_at}, riot_account_id={self.riot_account_id})"

    def __eq__(self, other: Self) -> bool:
        return (
            self.tier == other.tier
            and self.rank == other.rank
            and self.leaguePoints == other.leaguePoints
        )

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Self) -> bool:
        if TIER_ORDER[self.tier] != TIER_ORDER[other.tier]:
            return TIER_ORDER[self.tier] < TIER_ORDER[other.tier]
        if RANK_ORDER[self.rank] != RANK_ORDER[other.rank]:
            return RANK_ORDER[self.rank] < RANK_ORDER[other.rank]
        return self.leaguePoints < other.leaguePoints

    def __le__(self, other: Self) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: Self) -> bool:
        if TIER_ORDER[self.tier] != TIER_ORDER[other.tier]:
            return TIER_ORDER[self.tier] > TIER_ORDER[other.tier]
        if RANK_ORDER[self.rank] != RANK_ORDER[other.rank]:
            return RANK_ORDER[self.rank] > RANK_ORDER[other.rank]
        return self.leaguePoints > other.leaguePoints

    def __ge__(self, other: Self) -> bool:
        return not self.__lt__(other)


# Cs Go models


class CsGoAccount(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: str = Field(max_length=100, unique=True)
    game_name: str = Field(max_length=100)
    discord_member_id: int = Field(
        sa_column=Column(Integer, ForeignKey("discordmember.id", ondelete="CASCADE"))
    )

    def __str__(self):
        return self.game_name

    def __repr__(self):
        return f"CsGoAccount(player_id={self.player_id}, game_name={self.game_name}, discord_member_id={self.discord_member_id})"


class CsGoStats(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: str
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
    created_at: datetime = Field(default=datetime.now)
    csgo_account_id: int = Field(
        sa_column=Column(Integer, ForeignKey("csgoaccount.id", ondelete="CASCADE"))
    )

    def __str__(self):
        return f"{self.player_id} - {self.rank}"

    def __repr__(self):
        return f"CsGoStats(player_id={self.player_id}, wins={self.wins}, losses={self.losses}, ties={self.ties}, rank={self.rank}, best_rank={self.best_rank}, kills={self.kills}, deaths={self.deaths}, assists={self.assists}, headshots={self.headshots}, damage={self.damage})"


# Create the database

engine = create_engine(SUPABASE_URL)
SQLModel.metadata.create_all(engine)

# Create a context manager for the session


@contextlib.contextmanager
def unit():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except BotException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise ValueError(f"Rolling back, cause : {str(e)}") from e
    finally:
        session.close()
