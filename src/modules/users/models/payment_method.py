from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, TimestampMixin

if TYPE_CHECKING:
    from .order import Order
    from .payment import Payment
    from .user import User

class PaymentMethod(TimestampMixin, Base):
    __tablename__ = "payment_methods"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    method_type: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    user: Mapped[User] = relationship(back_populates="payment_methods")
    orders: Mapped[list[Order]] = relationship(back_populates="payment_method")
    payments: Mapped[list[Payment]] = relationship(back_populates="payment_method")
