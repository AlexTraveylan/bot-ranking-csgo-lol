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
    discord_real_name: str = Field(max_length=100)


class RiotAccount(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_name: str = Field(max_length=100)
    tag_line: str = Field(max_length=100, default="euw")
    puuid: str = Field(max_length=100)
    summoner_id: str = Field(max_length=100)
    discord_member_id: int = Field(
        sa_column=Column(Integer, ForeignKey("discordmember.id", ondelete="CASCADE"))
    )


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
