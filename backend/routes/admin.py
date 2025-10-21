from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import backend.app.models as models
import backend.app.schemas as schemas
from backend.app.database import get_db
from backend.dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/sellers", response_model=list[schemas.UserResponse])
def list_sellers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view sellers")
    return db.query(models.User).filter(models.User.role == "seller").all()


@router.post("/verify/{seller_id}")
def verify_seller(
    seller_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can verify sellers")

    seller = db.query(models.User).filter(models.User.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    seller.is_verified = True
    seller.verification_status = "approved"
    db.commit()
    db.refresh(seller)

    return {"message": f"Seller {seller.username} verified successfully"}
