# at top: remove direct GenerativeModel usage
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.dependencies import get_current_user
import backend.app.models as models
import backend.app.ai as ai
import os, uuid, random, io
from pathlib import Path

router = APIRouter(prefix="/ar", tags=["ar"])

UPLOAD_DIR = Path("static/ar_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/suggest")
async def suggest_art_for_wall(
    wall: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        # Save wall image
        filename = f"{uuid.uuid4()}_{wall.filename}"
        dest = UPLOAD_DIR / filename
        b = await wall.read()
        with open(dest, "wb") as f:
            f.write(b)

        artworks = db.query(models.Artwork).all()
        if not artworks:
            raise HTTPException(status_code=404, detail="No artworks found in catalog")

        info = "\n".join([f"{a.id}: {a.title} (₹{a.price}) - {a.description}" for a in artworks])

        prompt = f"""Analyze this wall photo and suggest 3 artworks from the catalog that best match colors/style.
Catalog:
{info}
Return only the IDs and titles of the top 3 recommendations."""
        text = ai._get_text_response([b, prompt])

        return {"wall_uploaded": f"/{dest.as_posix()}", "recommendations": (text or "").strip()}
    except Exception as e:
        random_picks = random.sample(db.query(models.Artwork).all(), k=min(3, db.query(models.Artwork).count()))
        return {
            "wall_uploaded": f"/{dest.as_posix()}" if 'dest' in locals() else None,
            "recommendations": f"⚠️ AI failed. Showing random picks.",
            "fallback": [{"id": art.id, "title": art.title, "price": art.price} for art in random_picks],
        }
