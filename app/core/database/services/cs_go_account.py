from sqlmodel import Session, select

from app.core.database.models import CsGoAccount
from app.core.database.repository import IdType, Repository


class CsGoAccountService(Repository[CsGoAccount]):
    def create(session: Session, item: CsGoAccount) -> CsGoAccount:
        session.add(item)
        session.flush()
        session.refresh(item)

        return item

    def get_by_id(session: Session, id_: IdType) -> CsGoAccount | None:
        account = session.get_one(CsGoAccount, id_)

        return account

    def get_by_discord_member_id(
        session: Session, discord_member_id: IdType
    ) -> list[CsGoAccount]:
        accounts = session.exec(
            select(CsGoAccount).where(
                CsGoAccount.discord_member_id == discord_member_id
            )
        )

        return accounts

    def get_all(session: Session) -> list[CsGoAccount]:
        accounts = session.exec(select(CsGoAccount)).all()

        return accounts

    def delete(session: Session, id_: IdType) -> bool:
        account = session.get_one(CsGoAccount, id_)

        if account is None:
            return False

        session.delete(account)

        return True
