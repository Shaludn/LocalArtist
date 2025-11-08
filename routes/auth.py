# backend/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pathlib import Path
from backend.app.database import get_db
import backend.app.auth_utils as auth_utils
import backend.app.models as models
import backend.app.schemas as schemas
import traceback, uuid

router = APIRouter(prefix="/auth", tags=["auth"])

PROOFS_DIR = Path("static/proofs")
PROOFS_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/register", response_model=schemas.UserResponse)
async def register(
    # Required core fields
    username: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),  # "seller" | "customer"
    # Optional fields
    preferred_language: str = Form("en"),
    latitude: float = Form(None),
    longitude: float = Form(None),
    address: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Enforce unique phone
        existing = db.query(models.User).filter(models.User.phone_number == phone_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone number already registered")

        proof_url = None
        if file:
            fname = f"{uuid.uuid4()}_{file.filename}"
            dest = PROOFS_DIR / fname
            with open(dest, "wb") as f:
                f.write(await file.read())
            proof_url = f"/static/proofs/{fname}"

        # OPTION C: Auto-detect GPS is required for seller (unless a document is uploaded)
        if role == "seller":
            has_document = proof_url is not None
            has_gps = (latitude is not None and longitude is not None)
            if not (has_document or has_gps):
                raise HTTPException(
                    status_code=400,
                    detail="For sellers: Location (auto-detected GPS) or a proof document is required at registration."
                )

        hashed_pw = auth_utils.hash_password(password)
        new_user = models.User(
            username=username,
            phone_number=phone_number,
            password=hashed_pw,
            role=role,
            preferred_language=preferred_language,
            latitude=latitude, longitude=longitude, address=address,
            proof_url=proof_url,
            is_verified=False,
            verification_status="pending" if role == "seller" else "verified",
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except Exception as e:
        traceback.print_exc()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.phone_number == user.phone_number).first()
    if not db_user or not auth_utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth_utils.create_access_token({"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
