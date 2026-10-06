from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import MONEY, Base, UpdatedTimestampMixin

if TYPE_CHECKING:
    from .cart_item import CartItem
    from .category import Category
    from .order_item import OrderItem
    from .stock_movement import StockMovement
    from .stock_receipt_item import StockReceiptItem

class Product(UpdatedTimestampMixin, Base):
    __tablename__ = "products"
    __table_args__ = (CheckConstraint("price >= 0", name="price_non_negative"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    category: Mapped[Category] = relationship(back_populates="products")
    cart_items: Mapped[list[CartItem]] = relationship(back_populates="product")
    order_items: Mapped[list[OrderItem]] = relationship(back_populates="product")
    stock_movements: Mapped[list[StockMovement]] = relationship(back_populates="product")
    stock_receipt_items: Mapped[list[StockReceiptItem]] = relationship(back_populates="product")
