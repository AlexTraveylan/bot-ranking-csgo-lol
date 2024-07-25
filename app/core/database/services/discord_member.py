from sqlmodel import Session, select
from typing_extensions import Literal

from app.core.database.models import DiscordMember
from app.core.database.repository import IdType, Repository


class DiscordMemberService(Repository[DiscordMember]):
    def create(session: Session, item: DiscordMember) -> DiscordMember:
        session.add(item)
        session.commit()
        session.refresh(item)

        return item

    def get_or_create(
        session: Session, discord_id: str, discord_name: str
    ) -> tuple[Literal["get", "create"], DiscordMember]:
        member = DiscordMemberService.get_by_discord_id(session, discord_id)

        if member is None:
            member = DiscordMember(discord_id=discord_id, discord_name=discord_name)
            member = DiscordMemberService.create(session, member)

            return "create", member

        return "get", member

    def get_by_id(session: Session, id_: IdType) -> DiscordMember | None:
        member = session.get_one(DiscordMember, id_)

        return member

    def get_by_discord_id(session: Session, discord_id: str) -> DiscordMember | None:
        member = session.exec(
            select(DiscordMember).where(DiscordMember.discord_id == discord_id)
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
