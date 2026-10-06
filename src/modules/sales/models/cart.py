from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, UpdatedTimestampMixin
if TYPE_CHECKING:
    from .cart_item import CartItem
    from .order import Order
    from .user import User

class Cart(UpdatedTimestampMixin, Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default="active")
    user: Mapped[User] = relationship(back_populates="carts")
    items: Mapped[list[CartItem]] = relationship(back_populates="cart", cascade="all, delete-orphan", passive_deletes=True)
    orders: Mapped[list[Order]] = relationship(back_populates="cart")
