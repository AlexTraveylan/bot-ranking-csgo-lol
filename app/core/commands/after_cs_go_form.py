from datetime import datetime
from typing import Literal, NoReturn

from sqlmodel import Session

from app.adapter.cs_go.scraping import get_player_info
from app.adapter.exception.bot_exception import UniqueConstraintException
from app.core.database.models import CsGoAccount, CsGoStats, DiscordMember, unit
from app.core.database.services.cs_go_account import CsGoAccountService
from app.core.database.services.discord_member import DiscordMemberService


class AfterCsGoForm:
    def __init__(
        self,
        steam_id: str,
        discord_author_id: int,
        discord_author_name: str,
        session: Session,
    ) -> None:
        self.steam_id = steam_id
        self.discord_author_id = discord_author_id
        self.discord_author_name = discord_author_name
        self.session = session
        self.is_member_exist: Literal["get", "create"]

    def __repr__(self) -> str:
        return f"AfterCsGoForm(steam_id={self.steam_id}, discord_author_id={self.discord_author_id}, discord_author_name={self.discord_author_name}, is_member_exist={self.is_member_exist})"

    def get_or_create_discord_member(self) -> DiscordMember:
        is_member_exist, member = DiscordMemberService.get_or_create(
            self.session, self.discord_author_id, self.discord_author_name
        )
        self.is_member_exist = is_member_exist

        return member

    def check_if_csgo_account_exist(self, member: DiscordMember) -> NoReturn | None:
        cs_go_accounts: list[CsGoAccount] = CsGoAccountService.get_by_discord_member_id(
            self.session, member.id
        )

        is_existing = any(
            self.steam_id == account.steam_id for account in cs_go_accounts
        )

        if is_existing is True:
            raise UniqueConstraintException(
                f"Player id {self.steam_id} already exists in the database"
            )

        return None

    def create(self, member: DiscordMember) -> tuple[CsGoAccount, CsGoStats]:
        stats = get_player_info(self.steam_id)

        db_account = CsGoAccount(
            steam_id=self.steam_id,
            game_name=stats.name,
            discord_member_id=member.id,
        )

        account_created = CsGoAccountService.create(self.session, db_account)

        stats_data = stats.to_dict_for_db(self.steam_id)
        db_stats = CsGoStats(
            **stats_data, csgo_account_id=account_created.id, created_at=datetime.now()
        )

        stats_created = CsGoAccountService.create(self.session, db_stats)

        return account_created, stats_created


if __name__ == "__main__":
    discord_id = "201103195877933057"
    discord_name = "ibushigin"
    IBUSHIN_ID = "76561198088442493"

    with unit() as session:
        form = AfterCsGoForm(IBUSHIN_ID, discord_id, discord_name, session)
        member = form.get_or_create_discord_member()
        form.check_if_csgo_account_exist(member)
        form.create(member)
