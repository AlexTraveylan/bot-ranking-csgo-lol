from sqlmodel import Session, select

from app.core.database.models import DiscordMember
from app.core.database.repository import IdType, Repository


class DiscordMemberController(Repository[DiscordMember]):
    def create(session: Session, item: DiscordMember) -> DiscordMember:
        session.add(item)
        session.commit()
        session.refresh(item)

        return item

    def get_by_id(session: Session, id_: IdType) -> DiscordMember | None:
        member = session.get_one(DiscordMember, id_)

        return member

    def get_by_name(session: Session, discord_real_name: str) -> DiscordMember | None:
        member = session.exec(
            select(DiscordMember).where(
                DiscordMember.discord_real_name == discord_real_name
            )
        ).first()

        return member

    def get_all(session: Session) -> list[DiscordMember]:
        members = session.exec(select(DiscordMember)).all()

        return members

    def delete(session: Session, id_: IdType) -> bool:
        member = session.get_one(DiscordMember, id_)

        if member is None:
            return False

        session.delete(member)

        return True
