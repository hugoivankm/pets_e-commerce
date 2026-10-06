from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, MONEY, UpdatedTimestampMixin
if TYPE_CHECKING:
    from .cart import Cart
    from .invoice import Invoice
    from .order_item import OrderItem
    from .payment import Payment
    from .payment_method import PaymentMethod
    from .user import User

class Order(UpdatedTimestampMixin, Base):
    __tablename__ = "orders"
    __table_args__ = (CheckConstraint("total_amount >= 0", name="total_amount_non_negative"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="pending")
    total_amount: Mapped[Decimal] = mapped_column(MONEY, nullable=False)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"), nullable=False, index=True)
    user: Mapped[User] = relationship(back_populates="orders")
    cart: Mapped[Cart] = relationship(back_populates="orders")
    payment_method: Mapped[PaymentMethod] = relationship(back_populates="orders")
    items: Mapped[list[OrderItem]] = relationship(back_populates="order", cascade="all, delete-orphan", passive_deletes=True)
    payments: Mapped[list[Payment]] = relationship(back_populates="order")
    invoice: Mapped[Invoice | None] = relationship(back_populates="order", uselist=False)
