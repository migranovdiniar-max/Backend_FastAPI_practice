from .base import Base, Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User


class Post(Base):
    titlee: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text, default="", server_default="", 
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="posts")