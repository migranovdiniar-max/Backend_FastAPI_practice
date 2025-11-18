from sqlalchemy import ForeignKey, UniqueConstraint

from api_v1.products.schemas import Product
from core.models.order import Order
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    count: Mapped[int] = mapped_column(default=1, server_default="1")
    # unit_price: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(back_populates='products_details')
    product: Mapped["Product"] = relationship(back_populates='orders_details')
