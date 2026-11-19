from flask import Blueprint, Response, g, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import DataError, IntegrityError, OperationalError

from src.modules.products.repositories.product_repo import (
    SqlAlchemyProductRepository,
)
from src.modules.products.schemas.product_schemas import (
    ProductCreateRequest,
    ProductResponse,
)
from src.modules.products.services.product_service import (
    ProductNotFoundError,
    ProductService,
)

product_bp = Blueprint("products", __name__)


@product_bp.get("/<int:product_id>")
def get_product(product_id: int) -> tuple[Response, int]:
    session = g.db_session
    repository = SqlAlchemyProductRepository(session)
    service = ProductService(repository=repository, session=session)

    try:
        product = service.get_product(product_id)
    except ProductNotFoundError as error:
        return jsonify({"error": str(error)}), 404

    response = ProductResponse.model_validate(product)
    return jsonify(response.model_dump(mode="json")), 200


@product_bp.post("", strict_slashes=False)
def create_product() -> tuple[Response, int]:
    session = g.db_session
    repository = SqlAlchemyProductRepository(session)
    service = ProductService(repository=repository, session=session)

    try:
        body = request.get_json()
        product = ProductCreateRequest.model_validate(body)
    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400

    try:
        result = service.create_product(
            name=product.name,
            sku=product.sku,
            category_id=product.category_id,
            price=product.price,
        )
    except IntegrityError:
        return jsonify({"error": "invalid data"}), 400
    except DataError:
        return jsonify({"error": "invalid data"}), 400
    except OperationalError:
        return jsonify({"error": "something went wrong"}), 500

    response = ProductResponse.model_validate(result)
    return jsonify(response.model_dump(mode="json")), 201
