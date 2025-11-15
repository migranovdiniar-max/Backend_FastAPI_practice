from core.models.mixins import UserRelationMixin
from .base import Base, Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    titlee: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text, default="", server_default="", 
    )
    