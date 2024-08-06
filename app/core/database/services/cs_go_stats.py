from sqlmodel import Session, select

from app.core.database.models import CsGoStats
from app.core.database.repository import IdType, Repository


class CsGoStatsService(Repository[CsGoStats]):
    def create(session: Session, item: CsGoStats) -> CsGoStats:
        session.add(item)
        session.flush()
        session.refresh(item)

        return item

    def get_by_id(session: Session, id_: IdType) -> CsGoStats | None:
        stats = session.get_one(CsGoStats, id_)

        return stats

    def get_last_score_by_csgo_account_id(
        session: Session, csgo_account_id: IdType
    ) -> CsGoStats:
        stats = session.exec(
            select(CsGoStats)
            .filter(CsGoStats.csgo_account_id == csgo_account_id)
            .order_by(CsGoStats.created_at.desc())
            .limit(1)
        ).first()

        return stats

    def get_all(session: Session) -> list[CsGoStats]:
        stats = session.exec(select(CsGoStats)).all()

        return stats

    def delete(session: Session, id_: IdType) -> bool:
        stats = session.get_one(CsGoStats, id_)

        if stats is None:
            return False

        session.delete(stats)

        return True
