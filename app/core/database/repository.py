from uuid import UUID

from pydantic import PositiveInt
from sqlmodel import Session

type IdType = PositiveInt | UUID


class Repository[T]:
    def create(session: Session, item: T) -> T:
        pass

    def get_by_id(session: Session, id_: IdType) -> T | None:
        pass

    def get_all(session: Session) -> list[T]:
        pass

    def delete(session: Session, id_: IdType) -> bool:
        pass
