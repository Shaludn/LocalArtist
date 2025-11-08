from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.dependencies import get_current_user
import backend.app.ai as ai
import backend.app.models as models

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/ask")
def chatbot_ask(question: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    artworks = db.query(models.Artwork).all()
    catalog = "\n".join([f"- {a.title}: {a.description} (₹{a.price})" for a in artworks])
    answer = ai.chat_reply(question, catalog)
    return {"answer": answer}
