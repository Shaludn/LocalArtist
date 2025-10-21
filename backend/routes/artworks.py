from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.models as models
import backend.app.schemas as schemas
from backend.dependencies import get_current_user
import backend.app.ai as ai

router = APIRouter(prefix="/artworks", tags=["artworks"])

@router.post("/", response_model=schemas.ArtworkResponse)
def create_artwork(
    artwork: schemas.ArtworkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can post artworks")

    # AI-assisted description & price
    description = artwork.description or ai.generate_description(artwork.title)
    price = artwork.price if artwork.price > 0 else ai.recommend_price(artwork.title)

    new_artwork = models.Artwork(
        title=artwork.title,
        description=description,
        price=price,
        image_url=artwork.image_url,
        owner_id=current_user.id,
    )
    db.add(new_artwork)
    db.commit()
    db.refresh(new_artwork)
    return new_artwork

@router.get("/", response_model=list[schemas.ArtworkResponse])
def list_artworks(db: Session = Depends(get_db)):
    return db.query(models.Artwork).all()
