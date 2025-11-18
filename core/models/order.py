from sqlalchemy import func

from core.models.order_product_association import OrderProductAssociation
from .base import Base, Mapped, mapped_column
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .product import Product


class Order(Base):
    promocode: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    
    products: Mapped[list["Product"]] = relationship(
        secondary="order_product_association",
        back_populates="orders",
        # lazy="noload"
    )

    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order",
    )
