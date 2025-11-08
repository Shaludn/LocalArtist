# backend/routes/artworks.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pathlib import Path
from backend.app.database import get_db
import backend.app.models as models
import backend.app.schemas as schemas
from backend.dependencies import get_current_user
import backend.app.ai as ai
from math import sin, cos, asin, sqrt, radians

router = APIRouter(prefix="/artworks", tags=["artworks"])

ART_DIR = Path("static/artworks")
ART_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/", response_model=schemas.ArtworkResponse)
async def create_artwork(
    title: str = Form(...),
    price: float = Form(0.0),
    description: str = Form(""),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can post artworks")

    # Read image
    raw = await image.read()

    # 1) Quality check; if bad -> auto-enhance -> recheck
    qc = ai.check_image_quality(raw)
    if qc == "REJECT_QUALITY_ISSUE":
        improved = ai.enhance_image(raw)
        qc2 = ai.check_image_quality(improved)
        if qc2 == "REJECT_QUALITY_ISSUE":
            raise HTTPException(status_code=400, detail="Image too unclear even after enhancement. Please upload a clearer, well-lit photo.")
        final_bytes = improved
    else:
        final_bytes = raw

    # 2) AI description/price if not provided
    final_description = description or ai.generate_description(title)
    final_price = float(price) if float(price) > 0 else ai.recommend_price(title, final_description)

    # 3) Save image
    filename = f"{current_user.id}_{image.filename}"
    dest = ART_DIR / filename
    with open(dest, "wb") as f:
        f.write(final_bytes)
    image_url = f"/static/artworks/{filename}"

    art = models.Artwork(
        title=title,
        description=final_description,
        price=final_price,
        image_url=image_url,
        owner_id=current_user.id,
    )
    db.add(art)
    db.commit()
    db.refresh(art)
    return art
