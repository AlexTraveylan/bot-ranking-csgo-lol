from sqlmodel import Session, select

from app.core.database.models import RiotAccount
from app.core.database.repository import IdType, Repository


class RiotAccountService(Repository[RiotAccount]):
    def create(session: Session, item: RiotAccount) -> RiotAccount:
        session.add(item)
        session.flush()
        session.refresh(item)

        return item

    def get_by_id(session: Session, id_: IdType) -> RiotAccount | None:
        account = session.get_one(RiotAccount, id_)

        return account

    def get_by_discord_member_id(
        session: Session, discord_member_id: IdType
    ) -> list[RiotAccount]:
        accounts = session.exec(
            select(RiotAccount).where(
                RiotAccount.discord_member_id == discord_member_id
            )
        )

        return accounts

    def get_all(session: Session) -> list[RiotAccount]:
        accounts = session.exec(select(RiotAccount)).all()

        return accounts

    def delete(session: Session, id_: IdType) -> bool:
        account = session.get_one(RiotAccount, id_)

        if account is None:
            return False

        session.delete(account)

        return True
