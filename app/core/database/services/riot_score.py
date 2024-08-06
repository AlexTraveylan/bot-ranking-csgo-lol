from sqlmodel import Session, select

from app.core.database.models import RiotScore
from app.core.database.repository import IdType, Repository


class RiotScoreService(Repository[RiotScore]):
    def create(session: Session, item: RiotScore) -> RiotScore:
        session.add(item)
        session.flush()
        session.refresh(item)

        return item

    def get_by_id(session: Session, id_: IdType) -> RiotScore | None:
        score = session.get_one(RiotScore, id_)

        return score

    def get_last_score_by_riot_account_id(
        session: Session, riot_account_id: IdType
    ) -> RiotScore:
        score = session.exec(
            select(RiotScore)
            .filter(RiotScore.riot_account_id == riot_account_id)
            .order_by(RiotScore.created_at.desc())
            .limit(1)
        ).first()

        return score

    def get_all(session: Session) -> list[RiotScore]:
        scores = session.exec(select(RiotScore)).all()

        return scores

    def delete(session: Session, id_: IdType) -> bool:
        score = session.get_one(RiotScore, id_)

        if score is None:
            return False

        session.delete(score)

        return True
