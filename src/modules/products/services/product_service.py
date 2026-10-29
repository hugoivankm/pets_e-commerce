from decimal import Decimal

from sqlalchemy.orm import Session

from src.modules.products.models import Product
from src.modules.products.repositories.product_repo import ProductRepository


class ProductNotFoundError(Exception):
    """Exception to convey the meaning the product specified was not found"""


class ProductService:
    def __init__(self, repository: ProductRepository, session: Session) -> None:
        self.repository = repository
        self.session = session

    def create_product(
        self, *, name: str, sku: str, category_id: int, price: Decimal
    ) -> Product:
        product = Product(name=name, sku=sku, category_id=category_id, price=price)
        try:
            self.repository.add(product)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return product

    def get_product(self, product_id: int) -> Product:
        result = self.repository.get_by_id(product_id)

        if result is None:
            raise ProductNotFoundError(f"Product with id {product_id} not found")
        return result
