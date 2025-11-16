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

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.titlee})"
    
    def __repr__(self):
        return str(self)