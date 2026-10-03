from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.sale import Sale
from ..models.user import User
from ..schemas.sale import SaleCreate
from ..security.auth import get_current_user
from ..services.sales import create_sale

router = APIRouter(prefix="/api/sales", tags=["sales"])


@router.get("")
def list_sales(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    sales = db.query(Sale).order_by(Sale.id.desc()).limit(100).all()
    return [
        {
            "id": s.id,
            "customer_id": s.customer_id,
            "user_id": s.user_id,
            "total": s.total,
            "status": s.status,
            "created_at": s.created_at,
        }
        for s in sales
    ]


@router.post("")
def new_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return create_sale(db, data, user.id)
