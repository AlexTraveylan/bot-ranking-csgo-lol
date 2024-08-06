from typing import Literal, NoReturn

from sqlmodel import Session

from app.adapter.cs_go.scraping import get_player_info
from app.adapter.exception.bot_exception import UniqueConstraintException
from app.core.database.models import CsGoAccount, CsGoStats, DiscordMember
from app.core.database.services.cs_go_account import CsGoAccountService
from app.core.database.services.discord_member import DiscordMemberService


class AfterCsGoForm:
    def __init__(
        self,
        player_id: str,
        discord_author_id: int,
        discord_author_name: str,
        session: Session,
    ) -> None:
        self.player_id = player_id
        self.discord_author_id = discord_author_id
        self.discord_author_name = discord_author_name
        self.session = session
        self.is_member_exist: Literal["get", "create"]

    def __repr__(self) -> str:
        return f"AfterCsGoForm(player_id={self.player_id}, discord_author_id={self.discord_author_id}, discord_author_name={self.discord_author_name}, is_member_exist={self.is_member_exist})"

    def get_or_create_discord_member(self) -> DiscordMember:
        is_member_exist, member = DiscordMemberService.get_or_create(
            self.session, self.discord_author_id, self.discord_author_name
        )
        self.is_member_exist = is_member_exist

        return member

    def check_if_csgo_account_exist(self) -> NoReturn | None:
        cs_go_accounts: list[CsGoAccount] = CsGoAccountService.get_by_discord_member_id(
            self.session, self.discord_author_id
        )

        is_existing = any(
            self.player_id == account.player_id for account in cs_go_accounts
        )

        if is_existing is True:
            raise UniqueConstraintException(
                f"Player id {self.player_id} already exists in the database"
            )

        return None

    def create(self, member: DiscordMember) -> CsGoAccount:
        stats = get_player_info(self.player_id)

        db_account = CsGoAccount(
            player_id=self.player_id,
            game_name=stats.name,
            discord_member_id=member.id,
        )

        account_created = CsGoAccountService.create(self.session, db_account)

        stats_data = stats.to_dict_for_db(self.player_id)
        db_stats = CsGoStats(**stats_data, csgo_account_id=account_created.id)

        CsGoAccountService.create(self.session, db_stats)

        return account_created
