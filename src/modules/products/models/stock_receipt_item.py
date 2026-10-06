from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, MONEY
if TYPE_CHECKING:
    from .product import Product
    from .stock_receipt import StockReceipt

class StockReceiptItem(Base):
    __tablename__ = "stock_receipt_items"
    __table_args__ = (UniqueConstraint("stock_receipt_id", "product_id", name="receipt_product"), CheckConstraint("quantity_received > 0", name="quantity_received_positive"), CheckConstraint("unit_cost >= 0", name="unit_cost_non_negative"))
    id: Mapped[int] = mapped_column(primary_key=True)
    stock_receipt_id: Mapped[int] = mapped_column(ForeignKey("stock_receipts.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    quantity_received: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    stock_receipt: Mapped[StockReceipt] = relationship(back_populates="items")
    product: Mapped[Product] = relationship(back_populates="stock_receipt_items")
