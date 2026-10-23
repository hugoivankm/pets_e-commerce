from decimal import Decimal
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.modules.products.models import Product
from src.modules.products.repositories.product_repo import (
    SqlAlchemyProductRepository,
)


def test_add_registers_product_without_ending_transaction() -> None:
    session = MagicMock(spec=Session)
    repository = SqlAlchemyProductRepository(session)

    product = Product(
        name="Rope toy",
        sku="ROPE-1",
        category_id=1,
        price=Decimal("12.50"),
    )

    repository.add(product)

    session.add.assert_called_once_with(product)
    session.commit.assert_not_called()
    session.rollback.assert_not_called()
