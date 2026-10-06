from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base, UpdatedTimestampMixin

if TYPE_CHECKING:
    from .product import Product

class Category(UpdatedTimestampMixin, Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    category_description: Mapped[str | None] = mapped_column(Text)
    products: Mapped[list[Product]] = relationship(back_populates="category")
