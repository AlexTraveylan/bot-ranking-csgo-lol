from datetime import datetime

from sqlmodel import Session

from app.adapter.exception.bot_exception import DatabaseException
from app.adapter.league_of_legend.api_league import (
    get_5x5_ranking,
    get_league_informations,
)
from app.core.database.models import RiotAccount, RiotScore
from app.core.database.services.riot_account import RiotAccountService
from app.core.database.services.riot_score import RiotScoreService


class RiotRanking:
    def __init__(self, session: Session) -> None:
        self.session = session

    def __repr__(self) -> str:
        return f"RiotRanking(session={self.session})"

    def get_riot_accounts(self) -> dict[int, RiotAccount]:
        try:
            riot_accounts = RiotAccountService.get_all(self.session)
            return {account.id: account for account in riot_accounts}
        except Exception as e:
            raise DatabaseException(
                "Error while getting all riot accounts from database"
            ) from e

    def get_last_riot_score_by_account(
        self, riot_accounts: list[RiotAccount]
    ) -> dict[int, RiotScore]:
        try:
            last_scores = {}
            for account in riot_accounts:
                last_score = RiotScoreService.get_last_score_by_riot_account_id(
                    self.session, account.id
                )
                last_scores[account.id] = last_score

            return last_scores

        except Exception as e:
            raise DatabaseException(
                "Error while getting last score from database"
            ) from e

    def register_actual_score_for_all_accounts(
        self, riot_accounts: list[RiotAccount]
    ) -> dict[int, RiotScore]:
        new_scores = {}
        try:
            for account in riot_accounts:
                league_info = get_league_informations(account.summoner_id)
                league_5x5 = get_5x5_ranking(league_info)

                riot_score = RiotScore(
                    tier=league_5x5.tier,
                    rank=league_5x5.rank,
                    leaguePoints=league_5x5.leaguePoints,
                    wins=league_5x5.wins,
                    losses=league_5x5.losses,
                    created_at=datetime.now(),
                    riot_account_id=account.id,
                )

                riot_score_created = RiotScoreService.create(self.session, riot_score)
                new_scores[account.id] = riot_score_created
        except Exception as e:
            raise DatabaseException(
                "Error while creating new score for all accounts"
            ) from e

        return new_scores
