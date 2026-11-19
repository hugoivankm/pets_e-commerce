from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    category_id: int
    description: str | None
    price: Decimal
    stock: int
    active: bool


class ProductCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    category_id: int = Field(gt=0)
    price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
