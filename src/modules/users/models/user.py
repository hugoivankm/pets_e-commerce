from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, UpdatedTimestampMixin

if TYPE_CHECKING:
    from .cart import Cart
    from .order import Order
    from .payment_method import PaymentMethod
    from .stock_receipt import StockReceipt

class User(UpdatedTimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, server_default="customer")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    carts: Mapped[list[Cart]] = relationship(back_populates="user", cascade="all, delete-orphan")
    payment_methods: Mapped[list[PaymentMethod]] = relationship(back_populates="user", cascade="all, delete-orphan")
    orders: Mapped[list[Order]] = relationship(back_populates="user")
    received_stock_receipts: Mapped[list[StockReceipt]] = relationship(back_populates="received_by_user", foreign_keys="StockReceipt.received_by")
