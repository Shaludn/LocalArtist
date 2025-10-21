from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.auth_utils as auth_utils
import backend.app.models as models
import backend.app.schemas as schemas
import traceback

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(models.User).filter(models.User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # --- VALIDATION FOR SELLER REGISTRATION ---
        if user.role == "seller" and (not user.proof_url or not (user.latitude and user.longitude)):
             raise HTTPException(
                status_code=400, 
                detail="Sellers must provide a proof document URL and location (lat/lon/address)."
             )
        # ------------------------------------------

        hashed_pw = auth_utils.hash_password(user.password)
        new_user = models.User(
            username=user.username,
            email=user.email,
            password=hashed_pw,
            role=user.role,
            
            # --- SAVING NEW FIELDS ---
            phone_number=user.phone_number,
            preferred_language=user.preferred_language,
            latitude=user.latitude,
            longitude=user.longitude,
            address=user.address,
            proof_url=user.proof_url, # Now used for GST/PAN document link
            # Set verification status only if proof is provided
            verification_status="pending" if user.proof_url else "unsubmitted"
            # -------------------------
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ... (login route remains the same)