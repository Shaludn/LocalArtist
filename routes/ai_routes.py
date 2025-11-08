# replace bodies to call helper functions
from fastapi import APIRouter, Depends
from backend.dependencies import get_current_user
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.ai as ai

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/translate")
def translate_text_endpoint(text: str, target_lang: str = "en", current_user=Depends(get_current_user)):
    # If you don't have translation implemented, reuse summarize as placeholder or add a translate prompt.
    out = ai._get_text_response([f"Translate to {target_lang}: {text}"])
    return {"original": text, "translated": out or text}

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

from fastapi import UploadFile, File

@router.post("/voice")
async def voice_artwork(file: UploadFile = File(...), lang: str = "hi-IN", current_user=Depends(get_current_user)):
    # If you had a voice pathway earlier, keep it or remove. Here we stub return to avoid crashes.
    return {"message": "Voice-to-design not implemented in this build."}
