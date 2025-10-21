from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.models as models
from backend.dependencies import get_current_user

router = APIRouter(prefix="/seller", tags=["seller"])

@router.post("/upload_additional_proof") # 👈 RENAMED ENDPOINT
async def upload_additional_proof( # 👈 Changed to async
    file: UploadFile = File(...),
    proof_type: str = "GST/PAN", # 👈 Added type for clarity
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can upload proof")

    # ⚠️ Placeholder: In production, save the file and get a secure URL.
    fake_url = f"/static/proofs/{current_user.id}_{proof_type}_{file.filename}"
    
    # Store the URL in the generic proof_url field for now. 
    # For multiple documents, a new 'SellerDocuments' model would be required.
    current_user.proof_url = fake_url 
    current_user.verification_status = "pending"

    db.commit()
    db.refresh(current_user)

    return {"message": f"{proof_type} proof uploaded, awaiting verification", "proof_url": fake_url}