"""Реализация модели 'Заметки"""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.models import User


class Video(Base):
    """Видеопотоки."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str]
    url: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="videos")

    def __str__(self) -> str:
        return f"Video #{self.id}"
