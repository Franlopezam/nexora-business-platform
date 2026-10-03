from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.product import Product
from ..models.sale import Sale, SaleItem
from ..models.inventory import InventoryMovement
from ..schemas.sale import SaleCreate
from .audit import record


def create_sale(db: Session, data: SaleCreate, user_id: int):
    products = {}
    total = 0.0

    for item in data.items:
        product = db.get(Product, item.product_id)
        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(400, f"Insufficient stock for {product.name}")
        products[item.product_id] = product
        total += product.price * item.quantity

    sale = Sale(customer_id=data.customer_id, user_id=user_id, total=total)
    db.add(sale)
    db.flush()

    for item in data.items:
        product = products[item.product_id]
        product.stock -= item.quantity
        db.add(SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            subtotal=product.price * item.quantity,
        ))
        db.add(InventoryMovement(
            product_id=product.id,
            user_id=user_id,
            movement_type="sale",
            quantity=-item.quantity,
            note=f"Sale #{sale.id}",
        ))

    record(db, user_id, "sale.created", "sale", f"Sale #{sale.id}")
    db.commit()
    db.refresh(sale)
    return sale
