from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
if TYPE_CHECKING:
    from .stock_receipt_item import StockReceiptItem
    from .supplier import Supplier
    from .user import User

class StockReceipt(Base):
    __tablename__ = "stock_receipts"
    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False, index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    received_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="received")
    supplier: Mapped[Supplier] = relationship(back_populates="stock_receipts")
    received_by_user: Mapped[User] = relationship(back_populates="received_stock_receipts", foreign_keys=[received_by])
    items: Mapped[list[StockReceiptItem]] = relationship(back_populates="stock_receipt", cascade="all, delete-orphan", passive_deletes=True)
