from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.audit import AuditLog
from ..models.user import User
from ..security.auth import require_roles

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("")
def logs(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "manager")),
):
    rows = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(200).all()
    return [
        {
            "id": x.id,
            "user_id": x.user_id,
            "action": x.action,
            "resource": x.resource,
            "details": x.details,
            "created_at": x.created_at,
        }
        for x in rows
    ]
