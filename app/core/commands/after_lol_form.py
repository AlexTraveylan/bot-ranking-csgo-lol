from datetime import datetime
from typing import NoReturn

from sqlmodel import Session
from typing_extensions import Literal

from app.adapter.exception.bot_exception import (
    RiotApiException,
    UniqueConstraintException,
)
from app.adapter.league_of_legend.api_league import (
    get_5x5_ranking,
    get_account_informations,
    get_league_informations,
    get_summoner_informations,
)
from app.adapter.league_of_legend.schema import LeagueOutputItem, RiotAccountInput
from app.core.database.models import DiscordMember, RiotAccount, RiotScore
from app.core.database.services.discord_member import DiscordMemberService
from app.core.database.services.riot_account import RiotAccountService
from app.core.database.services.riot_score import RiotScoreService


class AfterLolForm:
    def __init__(
        self,
        summoner_name: str,
        discord_author_id: str,
        discord_author_name: str,
        session: Session,
    ) -> None:
        self.summoner_name = summoner_name
        self.discord_author_id = discord_author_id
        self.discord_author_name = discord_author_name
        self.session = session
        self.is_member_exist: Literal["get", "create"]

    def __repr__(self) -> str:
        return f"AfterLolForm(summoner_name={self.summoner_name}, discord_author_id={self.discord_author_id}, discord_author_name={self.discord_author_name}, is_member_exist={self.is_member_exist})"

    def get_or_create_discord_member(self) -> DiscordMember:
        is_member_exist, member = DiscordMemberService.get_or_create(
            self.session, self.discord_author_id, self.discord_author_name
        )
        self.is_member_exist = is_member_exist

        return member

    def check_if_riot_account_exist(self, member: DiscordMember) -> NoReturn | None:
        riot_accounts: list[RiotAccountInput] = (
            RiotAccountService.get_by_discord_member_id(self.session, member.id)
        )

        is_existing = any(
            self.summoner_name == account.game_name for account in riot_accounts
        )

        if is_existing:
            raise UniqueConstraintException(
                "Riot account already exists for this member"
            )

        return None

    def create_riot_account(self, member: DiscordMember) -> RiotAccount:
        riot_input = RiotAccountInput(game_name=self.summoner_name)

        try:
            lol_account_info = get_account_informations(riot_input)
            summoner_info = get_summoner_informations(lol_account_info.puuid)
        except Exception as e:
            raise RiotApiException(
                "An error occured while fetching data from Riot API"
            ) from e

        riot_account = RiotAccount(
            game_name=lol_account_info.gameName,
            tag_line=lol_account_info.tagLine,
            puuid=lol_account_info.puuid,
            summoner_id=summoner_info.id,
            discord_member_id=member.id,
        )

        riot_account_created = RiotAccountService.create(self.session, riot_account)

        return riot_account_created

    def create_riot_score(self, summoner_id: str, riot_account_id: int) -> RiotScore:
        try:
            league_info = get_league_informations(summoner_id)
        except Exception as e:
            raise RiotApiException(
                "An error occured while fetching data from Riot API"
            ) from e

        league_5x5: LeagueOutputItem = get_5x5_ranking(league_info)

        riot_score = RiotScore(
            tier=league_5x5.tier,
            rank=league_5x5.rank,
            leaguePoints=league_5x5.leaguePoints,
            wins=league_5x5.wins,
            losses=league_5x5.losses,
            created_at=datetime.now(),
            riot_account_id=riot_account_id,
        )

        riot_score_created = RiotScoreService.create(self.session, riot_score)

        return riot_score_created
