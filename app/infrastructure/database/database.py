from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True
    id: Any

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
