from typing import Protocol

from sqlalchemy.orm import Session

from src.modules.products.models import Product


class ProductRepository(Protocol):
    # We used it to define a protocol for product repositories
    def add(self, product: Product) -> None: ...

    def get_by_id(self, product_id: int) -> Product | None: ...


class SqlAlchemyProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> None:
        self.session.add(product)

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)
