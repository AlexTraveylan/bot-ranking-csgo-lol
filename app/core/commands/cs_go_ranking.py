import logging
from datetime import datetime

from sqlmodel import Session

from app.adapter.cs_go.schemas import CsStatsInfoSchema
from app.adapter.cs_go.scraping import get_player_info
from app.adapter.exception.bot_exception import DatabaseException
from app.core.database.models import CsGoAccount, CsGoStats
from app.core.database.services.cs_go_account import CsGoAccountService
from app.core.database.services.cs_go_stats import CsGoStatsService

logger = logging.getLogger(__name__)


class CsGoRanking:
    def __init__(self, session: Session) -> None:
        self.session = session

    def __repr__(self) -> str:
        return f"CsGoRanking(session={self.session})"

    def get_csgo_accounts(self) -> dict[int, CsGoAccount]:
        try:
            csgo_accounts = CsGoAccountService.get_all(self.session)
            return {account.id: account for account in csgo_accounts}
        except Exception as e:
            raise DatabaseException(
                "Error while getting all csgo accounts from database"
            ) from e

    def get_last_cs_go_score_by_account(
        self, csgo_accounts: list[CsGoAccount]
    ) -> dict[int, CsGoStats]:
        try:
            last_scores = {}
            for account in csgo_accounts:
                last_score = CsGoStatsService.get_last_score_by_csgo_account_id(
                    self.session, account.id
                )
                last_scores[account.id] = last_score

            return last_scores
        except Exception as e:
            raise DatabaseException(
                "Error while getting last score from database"
            ) from e

    def register_actual_score_for_all_accounts(
        self, csgo_accounts: list[CsGoAccount]
    ) -> dict[int, CsGoStats]:
        new_scores = {}
        try:
            for account in csgo_accounts:
                try:
                    cs_stats_info = get_player_info(account.steam_id)
                except Exception as e:
                    logger.exception(e)
                    cs_stats_info = CsStatsInfoSchema.from_no_data()

                db_stats = CsGoStats(
                    **cs_stats_info.to_dict_for_db(account.steam_id),
                    csgo_account_id=account.id,
                    created_at=datetime.now(),
                )

                stats_created = CsGoStatsService.create(self.session, db_stats)
                new_scores[account.id] = stats_created

        except Exception as e:
            raise DatabaseException(
                "Error while creating new stats for all csgo account"
            ) from e

        return new_scores
