"""Schema-level tests for sales models; no database connection is used."""

from src.modules.sales import Cart, CartItem, Invoice, Order, OrderItem, Payment, Refund


def _check_constraint_sql(model: type) -> set[str]:
    return {
        str(constraint.sqltext)
        for constraint in model.__table__.constraints
        if hasattr(constraint, "sqltext")
    }


def test_cart_item_requires_positive_quantity_and_non_negative_price() -> None:
    checks = _check_constraint_sql(CartItem)

    assert "quantity > 0" in checks
    assert "unit_price >= 0" in checks


def test_order_item_preserves_one_row_per_product_and_valid_quantity() -> None:
    constraints = OrderItem.__table__.constraints
    checks = _check_constraint_sql(OrderItem)
    unique_pairs = {
        tuple(column.name for column in constraint.columns)
        for constraint in constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    }

    assert "quantity > 0" in checks
    assert "unit_price >= 0" in checks
    assert ("order_id", "product_id") in unique_pairs


def test_order_total_and_payment_amount_constraints() -> None:
    assert "total_amount >= 0" in _check_constraint_sql(Order)
    assert "amount > 0" in _check_constraint_sql(Payment)
    assert "amount > 0" in _check_constraint_sql(Refund)


def test_invoice_is_unique_per_order_and_invoice_number_is_unique() -> None:
    invoice_table = Invoice.__table__

    assert invoice_table.c.order_id.unique is True
    assert invoice_table.c.invoice_number.unique is True


def test_cart_uses_expected_table_name() -> None:
    assert Cart.__tablename__ == "carts"
