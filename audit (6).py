from sqlalchemy.orm import Session
from ..models.audit import AuditLog


def record(db: Session, user_id: int | None, action: str, resource: str, details: str = ""):
    db.add(AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        details=details[:500],
    ))
