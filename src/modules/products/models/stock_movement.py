from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, TimestampMixin
if TYPE_CHECKING:
    from .product import Product

class StockMovement(TimestampMixin, Base):
    __tablename__ = "stock_movements"
    __table_args__ = (CheckConstraint("quantity_change <> 0", name="quantity_change_non_zero"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    quantity_change: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    reference_type: Mapped[str | None] = mapped_column(String(100))
    reference_id: Mapped[int | None] = mapped_column(Integer)
    product: Mapped[Product] = relationship(back_populates="stock_movements")
