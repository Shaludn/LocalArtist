from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.models as models
import backend.app.schemas as schemas
from backend.dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=schemas.NotificationResponse)
def create_notification(
    user_id: int,
    message: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create notifications")

    new_note = models.Notification(user_id=user_id, message=message)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/my", response_model=list[schemas.NotificationResponse])
def my_notifications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Notification).filter(models.Notification.user_id == current_user.id).all()
