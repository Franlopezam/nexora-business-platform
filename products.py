from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.product import Product
from ..models.user import User
from ..schemas.product import ProductCreate, ProductOut
from ..security.auth import get_current_user, require_roles
from ..services.audit import record

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    q: str = "",
    low_stock: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Product)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Product.name.ilike(like), Product.sku.ilike(like)))
    if low_stock:
        query = query.filter(Product.stock <= Product.min_stock)
    return query.order_by(Product.id.desc()).all()


@router.post("", response_model=ProductOut)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin", "manager")),
):
    if db.query(Product).filter(Product.sku == data.sku).first():
        raise HTTPException(409, "SKU already exists")
    product = Product(**data.model_dump())
    db.add(product)
    record(db, user.id, "product.created", "product", data.sku)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin")),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    db.delete(product)
    record(db, user.id, "product.deleted", "product", product.sku)
    db.commit()
    return {"message": "Product deleted"}
