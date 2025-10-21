# backend/routes/chatbot.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.dependencies import get_current_user
import backend.app.ai as ai
import backend.app.models as models

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/ask")
def chatbot_ask(
    question: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Fetch artworks from DB for context
    artworks = db.query(models.Artwork).all()
    artworks_info = "\n".join([f"- {a.title}: {a.description} (${a.price})" for a in artworks])

    prompt = f"""
    You are an assistant for a marketplace of handmade artisan products.
    The customer asked: "{question}"

    Here are some artworks available:
    {artworks_info}

    Recommend the best options in a friendly way.
    """
    response = ai.model.generate_content(prompt)
    return {"answer": response.text.strip()}
