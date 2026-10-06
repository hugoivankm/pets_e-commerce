"""Tests that all model modules register with the shared SQLAlchemy metadata."""

from sqlalchemy.orm import configure_mappers

from src.core import Base
import src.modules  # noqa: F401 - imports every mapped model for registration


def test_all_domain_models_are_registered_in_shared_metadata() -> None:
    assert set(Base.metadata.tables) == {
        "cart_items",
        "carts",
        "categories",
        "invoices",
        "order_items",
        "orders",
        "payment_methods",
        "payments",
        "products",
        "refunds",
        "stock_movements",
        "stock_receipt_items",
        "stock_receipts",
        "suppliers",
        "users",
    }


def test_all_model_relationships_can_be_configured() -> None:
    # Raises if a relationship target or back_populates declaration is invalid.
    configure_mappers()
