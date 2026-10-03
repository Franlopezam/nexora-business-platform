from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.customer import Customer
from ..models.product import Product
from ..models.sale import Sale
from ..models.user import User
from ..security.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    revenue = db.query(func.coalesce(func.sum(Sale.total), 0)).filter(Sale.status == "completed").scalar()
    products = db.query(Product).count()
    customers = db.query(Customer).count()
    low_stock = db.query(Product).filter(Product.stock <= Product.min_stock).count()
    sales = db.query(Sale).count()

    return {
        "revenue": round(float(revenue), 2),
        "products": products,
        "customers": customers,
        "low_stock": low_stock,
        "sales": sales,
    }
