import contextlib
from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlmodel import Field, Session, SQLModel

from app.adapter.exception.bot_exception import DatabaseException


class BaseSQLModel(SQLModel):
    model_config = ConfigDict(validate_assignment=True)


class DiscordMember(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    discord_real_name: str = Field(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.discord_real_name

    def __repr__(self):
        return (
            f"DiscordMember(id={self.id}, discord_real_name={self.discord_real_name})"
        )


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


# Create the database

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Create a context manager for the session


@contextlib.contextmanager
def unit():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise DatabaseException(f"Rolling back, cause : {str(e)}") from e
    finally:
        session.close()
