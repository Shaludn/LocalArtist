# backend/routes/seller_ai.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.models as models
from backend.dependencies import get_current_user
import backend.app.ai as ai

router = APIRouter(prefix="/seller_ai", tags=["seller_ai"])

@router.get("/trending")
def get_trending_designs(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can see trending designs")

    suggestions = ai.suggest_trending_designs()
    return {"seller": current_user.username, "trending_designs": suggestions}
