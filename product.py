from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=150)
    description: str = ""
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    min_stock: int = Field(ge=0)


class ProductOut(ProductCreate):
    id: int

    model_config = {"from_attributes": True}
