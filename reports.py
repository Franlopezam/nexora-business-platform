import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.sale import Sale
from ..models.user import User
from ..security.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/sales.csv")
def sales_csv(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "customer_id", "user_id", "total", "status", "created_at"])

    for sale in db.query(Sale).order_by(Sale.id.desc()).all():
        writer.writerow([
            sale.id, sale.customer_id, sale.user_id, sale.total,
            sale.status, sale.created_at.isoformat()
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=nexora-sales.csv"},
    )
