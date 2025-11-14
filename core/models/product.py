from .base import Base, Mapped, mapped_column


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()