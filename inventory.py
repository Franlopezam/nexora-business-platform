from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.inventory import InventoryMovement
from ..models.product import Product
from ..models.user import User
from ..security.auth import get_current_user
from ..services.audit import record

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


class MovementCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    movement_type: str = "restock"
    note: str = ""


@router.get("")
def movements(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(InventoryMovement).order_by(InventoryMovement.id.desc()).limit(100).all()
    return [r.__dict__ | {"_sa_instance_state": None} for r in rows]


@router.post("")
def create_movement(
    data: MovementCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = db.get(Product, data.product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    delta = data.quantity if data.movement_type == "restock" else -data.quantity
    if product.stock + delta < 0:
        raise HTTPException(400, "Stock cannot become negative")

    product.stock += delta
    movement = InventoryMovement(
        product_id=product.id,
        user_id=user.id,
        movement_type=data.movement_type,
        quantity=delta,
        note=data.note,
    )
    db.add(movement)
    record(db, user.id, "inventory.movement", "product", str(product.id))
    db.commit()
    db.refresh(movement)
    return movement
