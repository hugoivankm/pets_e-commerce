from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.modules.products.models import Product
from src.modules.products.services.product_service import (
    ProductNotFoundError,
    ProductService,
)


class FakeProductRepository:
    def __init__(self):
        self.products: list[Product] = []

    def add(self, product: Product) -> None:
        self.products.append(product)

    def get_by_id(self, product_id: int) -> Product | None:
        for p in self.products:
            if p.id == product_id:
                return p
        return None


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


def test_get_product_by_id_returns_a_valid_product() -> None:
    repository = FakeProductRepository()
    session = MagicMock(spec=Session)
    service = ProductService(repository=repository, session=session)

    p = Product(
        id=1,
        name="Rope toy",
        sku="ROPE-1",
        category_id=1,
        price=Decimal("12.50"),
    )

    repository.add(p)
    result = service.get_product(1)

    assert result is p


def test_get_product_raises_when_missing() -> None:
    repository = FakeProductRepository()
    session = MagicMock(spec=Session)
    service = ProductService(repository=repository, session=session)

    with pytest.raises(ProductNotFoundError):
        _ = service.get_product(1)
