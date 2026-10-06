from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, MONEY, TimestampMixin
if TYPE_CHECKING:
    from .order import Order

class Invoice(TimestampMixin, Base):
    __tablename__ = "invoices"
    __table_args__ = (CheckConstraint("total >= 0", name="total_non_negative"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True, nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    total: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="issued")
    order: Mapped[Order] = relationship(back_populates="invoice")
