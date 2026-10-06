from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, MONEY, TimestampMixin
if TYPE_CHECKING:
    from .order import Order
    from .payment_method import PaymentMethod
    from .refund import Refund

class Payment(TimestampMixin, Base):
    __tablename__ = "payments"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="pending")
    reference: Mapped[str | None] = mapped_column(String(255), unique=True)
    amount: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    order: Mapped[Order] = relationship(back_populates="payments")
    payment_method: Mapped[PaymentMethod] = relationship(back_populates="payments")
    refunds: Mapped[list[Refund]] = relationship(back_populates="payment")
