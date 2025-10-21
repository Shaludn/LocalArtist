from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.models as models
import backend.app.schemas as schemas
from backend.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    artwork_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can place orders")

    artwork = db.query(models.Artwork).filter(models.Artwork.id == artwork_id).first()
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")

    new_order = models.Order(
        customer_id=current_user.id,
        artwork_id=artwork.id,
        quantity=quantity,
        status="pending",
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/my", response_model=list[schemas.OrderResponse])
def my_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can view their orders")
    return db.query(models.Order).filter(models.Order.customer_id == current_user.id).all()

@router.get("/sales", response_model=list[schemas.OrderResponse])
def my_sales(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view sales")
    return (
        db.query(models.Order)
        .join(models.Artwork)
        .filter(models.Artwork.owner_id == current_user.id)
        .all()
    )

@router.post("/{order_id}/update_status", response_model=schemas.OrderResponse)
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    artwork = db.query(models.Artwork).filter(models.Artwork.id == order.artwork_id).first()
    if current_user.role == "seller" and artwork.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot update this order")

    order.status = status
    db.commit()
    db.refresh(order)
    return order
