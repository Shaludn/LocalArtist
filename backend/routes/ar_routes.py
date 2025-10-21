from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.dependencies import get_current_user
import backend.app.models as models
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os
import uuid
import random

router = APIRouter(prefix="/ar", tags=["ar"])

# Configure Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-flash")

UPLOAD_DIR = "static/ar_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/suggest")
async def suggest_art_for_wall(
    wall: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        # Save wall image
        filename = f"{uuid.uuid4()}_{wall.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(await wall.read())

        # Load artworks from DB
        artworks = db.query(models.Artwork).all()
        if not artworks:
            raise HTTPException(status_code=404, detail="No artworks found in catalog")

        artworks_info = "\n".join(
            [f"{a.id}: {a.title} (${a.price}) - {a.description}" for a in artworks]
        )

        # Prepare input for Gemini (multimodal: image + text)
        with open(filepath, "rb") as f:
            wall_bytes = f.read()

        wall_image = Part.from_data(mime_type="image/jpeg", data=wall_bytes)

        prompt = f"""
        Analyze this wall photo and suggest 3 artworks from the catalog that would best match
        the style, colors, or theme of the wall.

        Catalog:
        {artworks_info}

        Return only the IDs and titles of the top 3 recommendations.
        """

        response = model.generate_content([wall_image, prompt])

        return {
            "wall_uploaded": f"/{filepath}",
            "recommendations": response.text.strip(),
        }

    except Exception as e:
        # Fallback: suggest 3 random artworks so demo never fails
        artworks = db.query(models.Artwork).all()
        random_picks = random.sample(artworks, min(3, len(artworks)))
        return {
            "wall_uploaded": f"/{filepath}" if "filepath" in locals() else None,
            "recommendations": f"⚠️ Gemini failed ({str(e)}). Here are random picks:",
            "fallback": [
                {"id": art.id, "title": art.title, "price": art.price}
                for art in random_picks
            ],
        }
