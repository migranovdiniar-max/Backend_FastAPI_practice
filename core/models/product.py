from core.models.order_product_association import OrderProductAssociation
from .base import Base, Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()

    orders: Mapped[list["Order"]] = relationship(
        secondary='order_product_association',
        back_populates="products",
    )

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",)
