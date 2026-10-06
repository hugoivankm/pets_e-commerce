"""Schema-level tests for product and inventory models; no database is used."""

from src.modules.products import (
    Category,
    Product,
    StockMovement,
    StockReceipt,
    StockReceiptItem,
)


def _check_constraint_sql(model: type) -> set[str]:
    return {
        str(constraint.sqltext)
        for constraint in model.__table__.constraints
        if hasattr(constraint, "sqltext")
    }


def test_product_has_unique_sku_and_non_negative_price_constraint() -> None:
    product_table = Product.__table__

    assert product_table.c.sku.unique is True
    assert "price >= 0" in _check_constraint_sql(Product)
    assert product_table.c.price.type.precision == 12
    assert product_table.c.price.type.scale == 2


def test_product_requires_a_category() -> None:
    category_id = Product.__table__.c.category_id

    assert category_id.nullable is False
    assert {foreign_key.target_fullname for foreign_key in category_id.foreign_keys} == {
        "categories.id"
    }


def test_stock_movements_must_change_stock_by_a_non_zero_amount() -> None:
    assert "quantity_change <> 0" in _check_constraint_sql(StockMovement)


def test_stock_receipt_item_enforces_quantity_cost_and_product_uniqueness() -> None:
    constraints = StockReceiptItem.__table__.constraints
    check_sql = _check_constraint_sql(StockReceiptItem)
    unique_pairs = {
        tuple(column.name for column in constraint.columns)
        for constraint in constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    }

    assert "quantity_received > 0" in check_sql
    assert "unit_cost >= 0" in check_sql
    assert ("stock_receipt_id", "product_id") in unique_pairs


def test_category_and_stock_receipt_models_use_expected_tables() -> None:
    assert Category.__tablename__ == "categories"
    assert StockReceipt.__tablename__ == "stock_receipts"
