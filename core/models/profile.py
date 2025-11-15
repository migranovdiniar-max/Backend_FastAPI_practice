from core.models.mixins import UserRelationMixin
from .base import Base, Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING


class Profile(UserRelationMixin, Base):
    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None] = mapped_column(String(255))
    _user_id_unique = True
    _user_back_populates = "profile"
