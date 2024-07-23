from sqlmodel import Session, select

from app.core.database.models import RiotScore
from app.core.database.repository import IdType, Repository


class RiotScoreController(Repository[RiotScore]):
    def create(session: Session, item: RiotScore) -> RiotScore:
        session.add(item)
        session.commit()
        session.refresh(item)

        return item

    def get_by_id(session: Session, id_: IdType) -> RiotScore | None:
        score = session.get_one(RiotScore, id_)

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
