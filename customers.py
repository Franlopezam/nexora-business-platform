from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.customer import Customer
from ..models.user import User
from ..schemas.customer import CustomerCreate, CustomerOut
from ..security.auth import get_current_user
from ..services.audit import record

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Customer).order_by(Customer.id.desc()).all()


@router.post("", response_model=CustomerOut)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.flush()
    record(db, user.id, "customer.created", "customer", str(customer.id))
    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    db.delete(customer)
    record(db, user.id, "customer.deleted", "customer", str(customer_id))
    db.commit()
    return {"message": "Customer deleted"}
