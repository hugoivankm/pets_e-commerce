from decimal import Decimal

from sqlalchemy.orm import Session

from src.modules.products.models import Product
from src.modules.products.repositories.product_repo import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository, session: Session) -> None:
        self.repository = repository
        self.session = session

    def create_product(
        self, *, name: str, sku: str, category_id: int, price: Decimal
    ) -> Product:
        product = Product(name=name, sku=sku, category_id=category_id, price=price)
        self.repository.add(product)
        return product
