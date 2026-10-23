from typing import Protocol

from sqlalchemy.orm import Session

from src.modules.products.models import Product


class ProductRepository(Protocol):
    def add(self, product: Product) -> None: ...


class SqlAlchemyProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> None:
        self.session.add(product)
