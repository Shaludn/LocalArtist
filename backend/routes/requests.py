from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.models as models
import backend.app.schemas as schemas
from backend.dependencies import get_current_user

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", response_model=schemas.RequestResponse)
def create_request(
    req: schemas.ArtworkBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can make requests")

    new_request = models.ArtRequest(
        title=req.title,
        description=req.description,
        requester_id=current_user.id,
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/", response_model=list[schemas.RequestResponse])
def list_requests(db: Session = Depends(get_db)):
    return db.query(models.ArtRequest).all() 
