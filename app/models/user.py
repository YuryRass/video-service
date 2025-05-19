"""Модель пользователей"""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.models import Video


class User(Base):
    """Пользователи."""

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    videos: Mapped[list["Video"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return f"User: {self.email}"
