from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.modules.products.models import Product
from src.modules.products.services.product_service import ProductService


class FakeProductRepository:
    def __init__(self):
        self.products: list[Product] = []

    def add(self, product: Product) -> None:
        self.products.append(product)


def test_create_product_stores_product() -> None:
    repository = FakeProductRepository()
    session = MagicMock(spec=Session)
    service = ProductService(repository=repository, session=session)

    product = service.create_product(
        name="Rope toy", sku="ROPE-1", category_id=1, price=Decimal("12.50")
    )

    assert repository.products == [product]
    assert product.name == "Rope toy"
    assert product.sku == "ROPE-1"
    assert product.category_id == 1
    assert product.price == Decimal("12.50")

    session.commit.assert_called_once()
    session.rollback.assert_not_called()


def test_create_product_rollsback_on_exception() -> None:
    repository = FakeProductRepository()
    session = MagicMock(spec=Session)
    service = ProductService(repository=repository, session=session)

    session.commit.side_effect = SQLAlchemyError()

    with pytest.raises(SQLAlchemyError):
        service.create_product(
            name="Rope toy",
            sku="ROPE-1",
            category_id=1,
            price=Decimal("12.50"),
        )

    session.rollback.assert_called_once_with()
