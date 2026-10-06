"""Domain modules and central SQLAlchemy model registration."""

# Import all mapped classes before metadata creation or mapper configuration.
from src.modules.products.models import (
    Category,
    Product,
    StockMovement,
    StockReceipt,
    StockReceiptItem,
    Supplier,
)
from src.modules.sales.models import Cart, CartItem, Invoice, Order, OrderItem, Payment, Refund
from src.modules.users.models import PaymentMethod, User

__all__ = [
    "Cart",
    "CartItem",
    "Category",
    "Invoice",
    "Order",
    "OrderItem",
    "Payment",
    "PaymentMethod",
    "Product",
    "Refund",
    "StockMovement",
    "StockReceipt",
    "StockReceiptItem",
    "Supplier",
    "User",
]
