# backend/routes/ai_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.ai as ai
from backend.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/translate")
def translate_text_endpoint(
    text: str, target_lang: str = "en", current_user=Depends(get_current_user)
):
    return {"original": text, "translated": ai.translate_text(text, target_lang)}

@router.post("/describe")
def describe_artwork(title: str, details: str = None, current_user=Depends(get_current_user)):
    return {"description": ai.generate_description(title, details)}

@router.post("/price")
def recommend_price_endpoint(title: str, description: str = "", current_user=Depends(get_current_user)):
    return {"recommended_price": ai.recommend_price(title, description)}

@router.post("/hashtags")
def hashtags_endpoint(description: str, current_user=Depends(get_current_user)):
    return {"hashtags": ai.suggest_hashtags(description)}

@router.post("/summarize")
def summarize_endpoint(description: str, current_user=Depends(get_current_user)):
    return {"summary": ai.summarize_artwork(description)}

# backend/routes/ai_routes.py

from fastapi import UploadFile, File
import backend.app.ai as ai

@router.post("/voice")
async def voice_artwork(
    file: UploadFile = File(...),
    lang: str = "hi-IN",
    current_user=Depends(get_current_user)
):
    audio_bytes = await file.read()
    result = ai.process_voice_artwork(audio_bytes, lang)
    return result

